from fastapi.testclient import TestClient
import datetime
from app import app

client = TestClient(app)


def test_create_form():
    response = client.post(
        "/createForm/",
        json={"clientID": "89662", "deadline": str(datetime.datetime.now())},
    )
    assert response.status_code == 200
