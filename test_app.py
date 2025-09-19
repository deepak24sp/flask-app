import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "message" in data
    assert data["message"] == "Welcome to Simple Flask API!"

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"

def test_get_todos(client):
    resp = client.get("/todos")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "todos" in data
    assert len(data["todos"]) >= 2

def test_create_todo(client):
    resp = client.post("/todos", json={"task": "Write tests"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["todo"]["task"] == "Write tests"

def test_update_todo(client):
    resp = client.put("/todos/1", json={"task": "Updated task", "completed": True})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["todo"]["completed"] is True

def test_delete_todo(client):
    resp = client.delete("/todos/1")
    assert resp.status_code in (200, 404)  # could already be deleted
