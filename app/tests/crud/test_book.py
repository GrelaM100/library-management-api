from sqlmodel import Session
from app.models.book import Book, BookCreate, BookBorrowUpdate
from app.crud.crud_book import create_book, delete_book, get_book_by_serial_number, get_all_books, update_book
from pydantic import ValidationError
import pytest
from datetime import datetime

from app.tests.utils import random_six_digit_number, create_random_book

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
    book = create_random_book(session=db)
    db_book = db.get(Book, book.id)
    assert db_book is not None

    deleted_book = delete_book(session=db, serial_number=book.serial_number)
    assert deleted_book is not None

    db_deleted_book = db.get(Book, deleted_book.id)
    assert db_deleted_book is None

def test_get_book_by_serial_number(db: Session) -> None:
    book = create_random_book(session=db)

    db_book = db.get(Book, book.id)
    assert db_book is not None

    fetched_book = get_book_by_serial_number(session=db, serial_number=book.serial_number)
    assert fetched_book is not None
    assert fetched_book.serial_number == book.serial_number

def test_get_all_books(db: Session) -> None:
    books = [
        create_random_book(session=db)
        for _ in range(3)
    ]

    all_books = get_all_books(session=db)
    assert len(all_books) == len(books)

    for book in books:
        assert any(b.serial_number == book.serial_number for b in all_books)

def test_borrow_book(db: Session) -> None:
    book = create_random_book(session=db)

    db_book = db.get(Book, book.id)
    assert db_book is not None
    assert db_book.is_borrowed == False
    assert db_book.borrowed_by == None
    assert db_book.borrowed_at == None

    borrow_id = random_six_digit_number()
    book_update = BookBorrowUpdate(
        is_borrowed=True,
        borrowed_by=borrow_id,
        borrowed_at=datetime.now()
    )
    updated_book = update_book(session=db, db_book=db_book, book_update=book_update)

    assert updated_book.is_borrowed == True
    assert updated_book.borrowed_by == borrow_id
    assert updated_book.borrowed_at is not None

    db_book = db.get(Book, book.id)
    assert db_book.is_borrowed == True
    assert db_book.borrowed_by == borrow_id
    assert db_book.borrowed_at is not None

def test_return_book(db: Session) -> None:
    book = create_random_book(session=db)

    borrow_id = random_six_digit_number()
    book_update = BookBorrowUpdate(
        is_borrowed=True,
        borrowed_by=borrow_id,
        borrowed_at=datetime.utcnow()
    )
    updated_book = update_book(session=db, db_book=book, book_update=book_update)

    assert updated_book.is_borrowed == True
    assert updated_book.borrowed_by == borrow_id
    assert updated_book.borrowed_at is not None

    book_return_update = BookBorrowUpdate(
        is_borrowed=False,
        borrowed_by=None,
        borrowed_at=None
    )
    returned_book = update_book(session=db, db_book=updated_book, book_update=book_return_update)

    assert returned_book.is_borrowed == False
    assert returned_book.borrowed_by == None
    assert returned_book.borrowed_at == None

    db_book = db.get(Book, book.id)
    assert db_book.is_borrowed == False
    assert db_book.borrowed_by == None
    assert db_book.borrowed_at == None