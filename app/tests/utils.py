import random

from sqlmodel import Session

from app.crud.crud_book import create_book
from app.models.book import Book, BookCreate


def random_six_digit_number():
    """
    Generate a random six-digit number as a string.

    Returns:
        str: A string representation of a random six-digit number.
    """
    number = random.randint(100000, 999999)
    return str(number)


def create_random_book(session: Session) -> Book:
    """
    Create a random book and add it to the database.

    Args:
        session (Session): The database session.

    Returns:
        Book: The created book with random serial number, title, and author.
    """
    serial_number = random_six_digit_number()
    book_create = BookCreate(
        serial_number=serial_number,
        title=f"Test Book {random_six_digit_number()}",
        author=f"Test Author {random_six_digit_number()}",
    )
    book = create_book(session=session, book_create=book_create)
    return book
