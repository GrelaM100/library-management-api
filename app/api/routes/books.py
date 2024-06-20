from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select, func
from sqlalchemy.exc import IntegrityError

from app.api.deps import SessionDep
from app.models.book import BookCreate, BookPublic, BooksPublic, BookBorrowUpdate, Book

router = APIRouter()

@router.post("/", response_model=BookPublic)
def create_book(*, session: SessionDep, book_create: BookCreate) -> Any:
    """
    Create a new book
    """    
    book = Book.model_validate(book_create)
    session.add(book)
    try:
        session.commit()
        session.refresh(book)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Book with this serial number already exists.")
    return book

@router.get("/", response_model=BooksPublic)
def get_all_books(*, session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all books
    """
    count_statement = select(func.count()).select_from(Book)
    count = session.exec(count_statement).one()
    statement = select(Book).offset(skip).limit(limit)
    books = session.exec(statement).all()

    return BooksPublic(data=books, count=count)
