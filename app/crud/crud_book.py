from sqlmodel import Session, select

from app.models.book import Book, BookCreate

def create_book(*, session: Session, book_create: BookCreate) -> Book:
    db_book = Book.model_validate(book_create)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book