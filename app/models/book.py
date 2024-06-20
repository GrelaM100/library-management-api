from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class BookBase(SQLModel):
    serial_number: str = Field(unique=True, index=True, schema_extra={'pattern': r'^\d{6}$'})
    title: str
    author: str
    is_borrowed: bool = False
    borrowed_by: Optional[str] = Field(default=None, schema_extra={'pattern': r'^\d{6}$'})
    borrowed_at: Optional[datetime] = None

class BookCreate(SQLModel):
    serial_number: str = Field(unique=True, index=True, schema_extra={'pattern': r'^\d{6}$'})
    title: str
    author: str

class BookBorrowUpdate(SQLModel):
    borrowed_by: Optional[str] = Field(schema_extra={'pattern': r'^\d{6}$'})
    borrowed_at: Optional[datetime] = None

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class BookPublic(SQLModel):
    serial_number: str
    title: str
    author: str
    is_borrowed: bool
    borrowed_by: Optional[str] = None
    borrowed_at: Optional[datetime] = None

class BooksPublic(SQLModel):
    data: list[BookPublic]
    count: int

class Message(SQLModel):
    message: str