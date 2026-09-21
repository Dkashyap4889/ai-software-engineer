import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_task():
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description", "status": "pending"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"
    assert "id" in data

def test_read_tasks_with_filter():
    client.post("/tasks/", json={"title": "Task 1", "status": "pending"})
    client.post("/tasks/", json={"title": "Task 2", "status": "completed"})

    response = client.get("/tasks/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task 1"

def test_validation_error():
    response = client.post("/tasks/", json={"description": "Missing title"})
    assert response.status_code == 422

def test_read_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_update_task():
    create_response = client.post("/tasks/", json={"title": "Old Title", "status": "pending"})
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New Title", "status": "in_progress"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "in_progress"

def test_delete_task():
    create_response = client.post("/tasks/", json={"title": "To Delete", "status": "pending"})
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
