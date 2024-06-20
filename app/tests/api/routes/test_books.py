from fastapi.testclient import TestClient

from app.core.config import settings

def test_create_book(client: TestClient) -> None:
    data = {
        "serial_number": "123456",
        "title": "Test Book",
        "author": "Test Author"
    }
    print(f"{settings.api_version_str}/books/")
    response = client.post(f"{settings.api_version_str}/books/", json=data)
    assert response.status_code == 200
    assert response.json()["serial_number"] == "123456"
    assert response.json()["title"] == "Test Book"
    assert response.json()["author"] == "Test Author"