from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_register_action():
    response = client.post(
        "/registerAction/",
        json={
            "formID": "3a3c3cd1-d6a4-4cee-9dbe-be2a0bc75afb",
            "action": "action_googleSheets",
            "trigger": "weekly",
            "meta": [{"meta_property": "sheet_name", "meta_value": "first_sheet"}],
        },
    )
    assert response.status_code == 200
