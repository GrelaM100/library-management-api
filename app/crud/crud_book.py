from sqlmodel import Session, select

from app.models.book import Book, BookCreate, BookBorrowUpdate
from app.exceptions import BookBorrowedError

def create_book(*, session: Session, book_create: BookCreate) -> Book:
    db_book = Book.model_validate(book_create)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

def delete_book(*, session: Session, serial_number: str) -> None:
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
    statement = select(Book).where(Book.serial_number == serial_number)
    db_book = session.exec(statement).first()
    return db_book

def get_all_books(session: Session) -> list[Book]:
    statement = select(Book)
    return session.exec(statement).all()

def update_book(*, session: Session, db_book: Book, book_update: BookBorrowUpdate) -> Book:
    book_data = book_update.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    
    session.commit()
    session.refresh(db_book)
    return db_book