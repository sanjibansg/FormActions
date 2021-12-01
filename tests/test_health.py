from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_healthcheck():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {
        "db_health": "up and running",
        "redis_health": "up and running",
    }
