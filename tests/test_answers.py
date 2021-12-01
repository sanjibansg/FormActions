from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_create_answer():
    response = client.post(
        "/createAnswer/",
        json={
            "questionID": "9c5681fd-9904-418f-822a-feb677de6bee",
            "answer": "New Delhi",
        },
    )
    assert response.status_code == 200
