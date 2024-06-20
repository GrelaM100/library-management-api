from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils import create_random_book

def test_create_book(client: TestClient) -> None:
    data = {
        "serial_number": "123456",
        "title": "Test Book",
        "author": "Test Author"
    }
    print(f"{settings.api_version_str}/books/")
    response = client.post(f"{settings.api_version_str}/books/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["serial_number"] == data["serial_number"]
    assert content["title"] == data["title"]
    assert content["author"] == data["author"]
    assert content["is_borrowed"] == False
    assert content["borrowed_by"] == None
    assert content["borrowed_at"] == None

def test_read_all_books(client: TestClient, db: Session) -> None:
    create_random_book(session=db)
    create_random_book(session=db)
    create_random_book(session=db)
    response = client.get(f"{settings.api_version_str}/books/")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 3

def test_read_book(client: TestClient, db: Session) -> None:
    book = create_random_book(session=db)
    response = client.get(f"{settings.api_version_str}/books/{book.serial_number}")
    assert response.status_code == 200
    content = response.json()
    assert content["serial_number"] == book.serial_number
    assert content["title"] == book.title
    assert content["author"] == book.author
    assert content["is_borrowed"] == book.is_borrowed
    assert content["borrowed_by"] == book.borrowed_by
    assert content["borrowed_at"] == book.borrowed_at

def test_read_book_not_found(client: TestClient) -> None:
    response = client.get(f"{settings.api_version_str}/books/123456")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Book not found"

def test_read_book_invalid_number(client: TestClient) -> None:
    response = client.get(f"{settings.api_version_str}/books/12345")
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Serial number must be a six-digit number"

def test_delete_book(client: TestClient, db: Session) -> None:
    book = create_random_book(session=db)
    response = client.delete(f"{settings.api_version_str}/books/{book.serial_number}")
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Book deleted successfully"

def test_delete_book_not_found(client: TestClient) -> None:
    response = client.delete(f"{settings.api_version_str}/books/123456")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Book not found"

def test_delete_book_borrowed(client: TestClient, db: Session) -> None:
    book = create_random_book(session=db)
    book.is_borrowed = True
    db.commit()
    response = client.delete(f"{settings.api_version_str}/books/{book.serial_number}")
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Cannot delete a borrowed book"