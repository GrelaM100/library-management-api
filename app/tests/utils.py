import random
from sqlmodel import Session
from app.models.book import BookCreate, Book
from app.crud.crud_book import create_book

def random_six_digit_number():
    number = random.randint(100000, 999999)
    return str(number)

def create_random_book(session: Session) -> Book:
    serial_number = random_six_digit_number()
    book_create = BookCreate(
        serial_number=serial_number,
        title=f"Test Book {random_six_digit_number()}",
        author=f"Test Author {random_six_digit_number()}"
    )
    book = create_book(session=session, book_create=book_create)
    return book