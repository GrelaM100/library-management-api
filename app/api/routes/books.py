from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import SessionDep
from app.models.book import BookCreate, BookPublic, Book

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