from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_create_question():
    response = client.post(
        "/createQuestion/",
        json={
            "formID": "3a3c3cd1-d6a4-4cee-9dbe-be2a0bc75afb",
            "question": "What is the capital of India?",
            "format": "short answer type",
        },
    )
    assert response.status_code == 200
