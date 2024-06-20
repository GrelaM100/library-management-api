from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session, delete

from app.core.db import engine, init_db
from app.models.book import Book


@pytest.fixture(scope="function", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Book)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
