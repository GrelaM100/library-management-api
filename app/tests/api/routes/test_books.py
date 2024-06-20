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

def test_get_all_books(client: TestClient, db: Session) -> None:
    create_random_book(session=db)
    create_random_book(session=db)
    create_random_book(session=db)
    response = client.get(f"{settings.api_version_str}/books/")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 3