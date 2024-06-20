from datetime import datetime

from sqlmodel import Session, select

from app.exceptions import BookBorrowedError
from app.models.book import Book, BookBorrowUpdate, BookCreate


def create_book(*, session: Session, book_create: BookCreate) -> Book:
    """
    Create a new book in the database.

    Args:
        session (Session): The database session.
        book_create (BookCreate): The data to create the book.

    Returns:
        Book: The created book.
    """
    db_book = Book.model_validate(book_create)
    db_book.is_borrowed = False
    db_book.borrowed_by = None
    db_book.borrowed_at = None
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


def delete_book(*, session: Session, serial_number: str) -> None:
    """
    Delete a book from the database by its serial number.

    Args:
        session (Session): The database session.
        serial_number (str): The serial number of the book to delete.

    Returns:
        None: If the book does not exist.
        Book: The deleted book.

    Raises:
        BookBorrowedError: If the book is currently borrowed.
    """
    statement = select(Book).where(Book.serial_number == serial_number)
    db_book = session.exec(statement).first()
    if not db_book:
        return None
    if db_book.is_borrowed:
        raise BookBorrowedError("Cannot delete a borrowed book")
    session.delete(db_book)
    session.commit()
    return db_book


def get_book_by_serial_number(*, session: Session, serial_number: str) -> Book:
    """
    Retrieve a book from the database by its serial number.

    Args:
        session (Session): The database session.
        serial_number (str): The serial number of the book to retrieve.

    Returns:
        Book: The book with the specified serial number.
    """
    statement = select(Book).where(Book.serial_number == serial_number)
    db_book = session.exec(statement).first()
    return db_book


def get_all_books(session: Session) -> list[Book]:
    """
    Retrieve all books from the database.

    Args:
        session (Session): The database session.

    Returns:
        list[Book]: A list of all books in the database.
    """
    statement = select(Book)
    return session.exec(statement).all()


def update_book(
    *, session: Session, db_book: Book, book_update: BookBorrowUpdate
) -> Book:
    """
    Update the details of a book in the database.

    Args:
        session (Session): The database session.
        db_book (Book): The existing book to update.
        book_update (BookBorrowUpdate): The data to update the book.

    Returns:
        Book: The updated book.
    """
    book_data = book_update.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)

    if book_update.borrowed_by:
        db_book.is_borrowed = True
        db_book.borrowed_at = book_update.borrowed_at or datetime.now()
    else:
        db_book.is_borrowed = False
        db_book.borrowed_at = None

    session.commit()
    session.refresh(db_book)
    return db_book
