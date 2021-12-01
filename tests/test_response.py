from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_create_response():
    response = client.post(
        "/createResponse/",
        json={
            "formID": "3a3c3cd1-d6a4-4cee-9dbe-be2a0bc75afb",
            "userID": "45665",
            "responses": ["859a9d82-8587-411a-bbfa-262037479385"],
        },
    )
    assert response.status_code == 200
