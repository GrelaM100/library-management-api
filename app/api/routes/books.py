from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select, func
from sqlalchemy.exc import IntegrityError

from app.api.deps import SessionDep
from app.models.book import BookCreate, BookPublic, BooksPublic, BookBorrowUpdate, Book, Message
from app.utils import validate_serial_number
from app.crud import crud_book
from app.exceptions import BookBorrowedError

router = APIRouter()

@router.post("/", response_model=BookPublic)
def create_book(*, session: SessionDep, book_create: BookCreate) -> Any:
    """
    Create a new book
    """    
    try:
        book = crud_book.create_book(session=session, book_create=book_create)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Book with this serial number already exists.")
    return book


@router.get("/", response_model=BooksPublic)
def read_all_books(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all books
    """
    books = crud_book.get_all_books(session=session)[skip:skip+limit]
    count_statement = select(func.count()).select_from(Book)
    count = session.exec(count_statement).one()
    return BooksPublic(data=books, count=count)

@router.get("/{serial_number}", response_model=BookPublic)
def read_book(session: SessionDep, serial_number: str) -> Any:
    """
    Get a specific book
    """
    validate_serial_number(serial_number)
    book = crud_book.get_book_by_serial_number(session=session, serial_number=serial_number)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{serial_number}")
def delete_book(session: SessionDep, serial_number: str) -> Message:
    """
    Delete a book
    """
    validate_serial_number(serial_number)
    try:
        book = crud_book.delete_book(session=session, serial_number=serial_number)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
    except BookBorrowedError:
        raise HTTPException(status_code=400, detail="Cannot delete a borrowed book")
    
    return Message(message="Book deleted successfully")

@router.put("/borrow/{serial_number}", response_model=BookPublic)
def borrow_book(*, session: SessionDep, serial_number: str, book_update: BookBorrowUpdate) -> Any:
    """
    Borrow a book
    """
    validate_serial_number(serial_number)
    book = crud_book.get_book_by_serial_number(session=session, serial_number=serial_number)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book is already borrowed")
 
    book = crud_book.update_book(session=session, db_book=book, book_update=book_update)
    return book

@router.put("/return/{serial_number}", response_model=BookPublic)
def return_book(*, session: SessionDep, serial_number: str) -> Any:
    """
    Return a borrowed book
    """
    validate_serial_number(serial_number)
    book = crud_book.get_book_by_serial_number(session=session, serial_number=serial_number)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_borrowed:
        raise HTTPException(status_code=400, detail="Book is not borrowed")
    book_update = BookBorrowUpdate(borrowed_by=None, borrowed_at=None)
    book = crud_book.update_book(session=session, db_book=book, book_update=book_update)
    return book