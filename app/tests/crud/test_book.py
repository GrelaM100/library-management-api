from sqlmodel import Session
from app.models.book import Book, BookCreate
from app.crud.crud_book import create_book, delete_book, get_book_by_serial_number, get_all_books
from pydantic import ValidationError
import pytest

from app.tests.utils import random_six_digit_number

def test_create_book(db: Session) -> None:
    serial_number = random_six_digit_number()
    book_create = BookCreate(
        serial_number=serial_number,
        title="Test Book",
        author="Test Author"
    )
    book = create_book(session=db, book_create=book_create)
    assert book.serial_number == serial_number
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.is_borrowed == False
    assert book.borrowed_by == None
    assert book.borrowed_at == None

    db_book = db.get(Book, book.id)
    assert db_book is not None
    assert db_book.serial_number == serial_number

def test_create_book_invalid_serial_number(db: Session) -> None:
    with pytest.raises(ValidationError):
        book_create = BookCreate(
            serial_number="12345",
            title="Test Book",
            author="Test Author"
        )
        create_book(session=db, book_create=book_create)

def test_delete_book(db: Session) -> None:
    serial_number = random_six_digit_number()
    book_create = BookCreate(
        serial_number=serial_number,
        title="Test Book",
        author="Test Author"
    )
    book = create_book(session=db, book_create=book_create)

    db_book = db.get(Book, book.id)
    assert db_book is not None

    deleted_book = delete_book(session=db, serial_number=serial_number)
    assert deleted_book is not None

    db_deleted_book = db.get(Book, deleted_book.id)
    assert db_deleted_book is None

def test_get_book_by_serial_number(db: Session) -> None:
    serial_number = random_six_digit_number()
    book_create = BookCreate(
        serial_number=serial_number,
        title="Test Book",
        author="Test Author"
    )
    book = create_book(session=db, book_create=book_create)

    db_book = db.get(Book, book.id)
    assert db_book is not None

    fetched_book = get_book_by_serial_number(session=db, serial_number=serial_number)
    assert fetched_book is not None
    assert fetched_book.serial_number == serial_number

def test_get_all_books(db: Session) -> None:
    serial_numbers = [random_six_digit_number() for _ in range(3)]
    book_creates = [
        BookCreate(serial_number=sn, title=f"Test Book {i+1}", author=f"Test Author {i+1}")
        for i, sn in enumerate(serial_numbers)
    ]

    for book_create in book_creates:
        create_book(session=db, book_create=book_create)

    all_books = get_all_books(session=db)
    assert len(all_books) == len(book_creates)

    for book_create in book_creates:
        assert any(book.serial_number == book_create.serial_number for book in all_books)
