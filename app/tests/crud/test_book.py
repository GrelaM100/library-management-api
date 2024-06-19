from sqlmodel import Session, select
from app.models.book import Book, BookCreate
from app.crud.crud_book import create_book
from pydantic import ValidationError
import pytest

def test_create_book(db: Session) -> None:
    book_create = BookCreate(
        serial_number="123456",
        title="Test Book",
        author="Test Author"
    )
    book = create_book(session=db, book_create=book_create)
    assert book.serial_number == "123456"
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.is_borrowed == False
    assert book.borrowed_by == None
    assert book.borrowed_at == None

    db_book = db.get(Book, book.id)
    assert db_book is not None
    assert db_book.serial_number == "123456"

def test_create_book_invalid_serial_number(db: Session) -> None:
    with pytest.raises(ValidationError):
        book_create = BookCreate(
            serial_number="12345",
            title="Test Book",
            author="Test Author"
        )
        create_book(session=db, book_create=book_create)
