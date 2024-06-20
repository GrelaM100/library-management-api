from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.crud import crud_book
from app.exceptions import BookBorrowedError
from app.models.book import (
    Book,
    BookBorrowUpdate,
    BookCreate,
    BookPublic,
    BooksPublic,
    Message,
)
from app.utils import validate_serial_number

router = APIRouter()


@router.post("/", response_model=BookPublic)
def create_book(*, session: SessionDep, book_create: BookCreate) -> Any:
    """
    Create a new book.

    Args:
        session (SessionDep): The database session.
        book_create (BookCreate): The book data to create.

    Returns:
        BookPublic: The created book.

    Raises:
        HTTPException: If a book with the same serial number already exists.
    """
    try:
        book = crud_book.create_book(session=session, book_create=book_create)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400, detail="Book with this serial number already exists."
        )
    return book


@router.get("/", response_model=BooksPublic)
def read_all_books(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve a list of all books.

    Args:
        session (SessionDep): The database session.
        skip (int, optional): Number of books to skip. Defaults to 0.
        limit (int, optional): Maximum number of books to retrieve. Defaults to 100.

    Returns:
        BooksPublic: The list of books and the total count.
    """
    books = crud_book.get_all_books(session=session)[skip : skip + limit]
    count_statement = select(func.count()).select_from(Book)
    count = session.exec(count_statement).one()
    return BooksPublic(data=books, count=count)


@router.get("/{serial_number}", response_model=BookPublic)
def read_book(session: SessionDep, serial_number: str) -> Any:
    """
    Retrieve the details of a specific book by its serial number.

    Args:
        session (SessionDep): The database session.
        serial_number (str): The serial number of the book to retrieve.

    Returns:
        BookPublic: The retrieved book.

    Raises:
        HTTPException: If the book is not found.
    """
    validate_serial_number(serial_number)
    book = crud_book.get_book_by_serial_number(
        session=session, serial_number=serial_number
    )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/borrow/{serial_number}", response_model=BookPublic)
def borrow_book(
    *, session: SessionDep, serial_number: str, book_update: BookBorrowUpdate
) -> Any:
    """
    Borrow a book.

    Args:
        session (SessionDep): The database session.
        serial_number (str): The serial number of the book to borrow.
        book_update (BookBorrowUpdate): The update data for the book.

    Returns:
        BookPublic: The updated book.

    Raises:
        HTTPException: If the book is not found or is already borrowed.
    """
    validate_serial_number(serial_number)
    book = crud_book.get_book_by_serial_number(
        session=session, serial_number=serial_number
    )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    book = crud_book.update_book(session=session, db_book=book, book_update=book_update)
    return book


@router.put("/return/{serial_number}", response_model=BookPublic)
def return_book(*, session: SessionDep, serial_number: str) -> Any:
    """
    Return a borrowed book.

    Args:
        session (SessionDep): The database session.
        serial_number (str): The serial number of the book to return.

    Returns:
        BookPublic: The updated book.

    Raises:
        HTTPException: If the book is not found or is not borrowed.
    """
    validate_serial_number(serial_number)
    book = crud_book.get_book_by_serial_number(
        session=session, serial_number=serial_number
    )
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book is not borrowed")
    book_update = BookBorrowUpdate(borrowed_by=None, borrowed_at=None)
    book = crud_book.update_book(session=session, db_book=book, book_update=book_update)
    return book


@router.delete("/{serial_number}")
def delete_book(session: SessionDep, serial_number: str) -> Message:
    """
    Delete a book.

    Args:
        session (SessionDep): The database session.
        serial_number (str): The serial number of the book to delete.

    Returns:
        Message: A message indicating the deletion status.

    Raises:
        HTTPException: If the book is not found or if the book is borrowed.
    """
    validate_serial_number(serial_number)
    try:
        book = crud_book.delete_book(session=session, serial_number=serial_number)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
    except BookBorrowedError:
        raise HTTPException(status_code=400, detail="Cannot delete a borrowed book")

    return Message(message="Book deleted successfully")
