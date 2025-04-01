import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import User, Task

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/testdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_user():
    return {"email": "test@example.com", "password": "testpass", "full_name": "Test User"}


@pytest.fixture
def test_task():
    return {"title": "Test Task", "description": "Test Description"}


def test_create_task(test_user, test_task):
    # Создаем пользователя
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 200

    # Логинимся для получения токена
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Создаем задачу
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/tasks/", json=test_task, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_task["title"]
    assert data["description"] == test_task["description"]
    assert "id" in data
