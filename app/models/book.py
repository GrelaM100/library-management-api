from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class BookBase(SQLModel):
    """
    Base class for Book model with common fields.

    Attributes:
        serial_number (str): Unique serial number of the book. Must be a 6-digit string.
        title (str): Title of the book.
        author (str): Author of the book.
        is_borrowed (bool): Indicates if the book is currently borrowed. Defaults to False.
        borrowed_by (Optional[str]): Library card number of the borrower. Must be a 6-digit string.
        borrowed_at (Optional[datetime]): Date and time when the book was borrowed.
    """

    serial_number: str = Field(
        unique=True, index=True, schema_extra={"pattern": r"^\d{6}$"}
    )
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_by: Optional[str] = Field(
        default=None, schema_extra={"pattern": r"^\d{6}$"}
    )
    borrowed_at: Optional[datetime] = None


class BookCreate(SQLModel):
    """
    Model for creating a new book.

    Attributes:
        serial_number (str): Unique serial number of the book. Must be a 6-digit string.
        title (str): Title of the book.
        author (str): Author of the book.
    """

    serial_number: str = Field(
        unique=True, index=True, schema_extra={"pattern": r"^\d{6}$"}
    )
    title: str
    author: str


class BookBorrowUpdate(SQLModel):
    """
    Model for updating the borrow status of a book.

    Attributes:
        borrowed_by (Optional[str]): Library card number of the borrower. Must be a 6-digit string.
        borrowed_at (Optional[datetime]): Date and time when the book was borrowed.
    """

    borrowed_by: Optional[str] = Field(schema_extra={"pattern": r"^\d{6}$"})
    borrowed_at: Optional[datetime] = None


class Book(BookBase, table=True):
    """
    Main Book model representing the book table in the database.

    Attributes:
        id (Optional[int]): Primary key of the book.
    """

    id: Optional[int] = Field(default=None, primary_key=True)


class BookPublic(SQLModel):
    """
    Public-facing Book model.

    Attributes:
        serial_number (str): Unique serial number of the book.
        title (str): Title of the book.
        author (str): Author of the book.
        is_borrowed (bool): Indicates if the book is currently borrowed.
        borrowed_by (Optional[str]): Library card number of the borrower.
        borrowed_at (Optional[datetime]): Date and time when the book was borrowed.
    """

    serial_number: str
    title: str
    author: str
    is_borrowed: bool
    borrowed_by: Optional[str] = None
    borrowed_at: Optional[datetime] = None


class BooksPublic(SQLModel):
    """
    Model for representing a list of public-facing books.

    Attributes:
        data (list[BookPublic]): List of public-facing book models.
        count (int): Total count of books.
    """

    data: list[BookPublic]
    count: int


class Message(SQLModel):
    """
    Model for representing a simple message.

    Attributes:
        message (str): The message content.
    """

    message: str
