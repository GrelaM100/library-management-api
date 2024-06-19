from sqlmodel import Session, select

from app.models.book import Book, BookCreate

def create_book(*, session: Session, book_create: BookCreate) -> Book:
    db_book = Book.model_validate(book_create)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

def delete_book(*, session: Session, serial_number: str) -> None:
    statement = select(Book).where(Book.serial_number == serial_number)
    db_book = session.exec(statement).first()
    if db_book:
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