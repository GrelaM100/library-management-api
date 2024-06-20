from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings
from app.models.book import Book

engine = create_engine(str(settings.sqlalchemy_database_uri))


def init_db(session: Session) -> None:
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    create_initial_books(session)


def create_initial_books(session: Session) -> None:
    books = [
        Book(serial_number="000001", title="Book One", author="Author One"),
        Book(serial_number="000002", title="Book Two", author="Author Two"),
        Book(serial_number="000003", title="Book Three", author="Author Three"),
    ]
    for book in books:
        session.add(book)
    session.commit()
