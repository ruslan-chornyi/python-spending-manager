from fastapi.testclient import TestClient
from api import app, get_current_user

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_expenses_without_key():
    response = client.get("/expenses")
    assert response.status_code == 422


def test_expenses_with_wrong_key():
    response = client.get("/expenses", headers={"X-API-Key": "wrong_key"})
    assert response.status_code == 401


def fake_user():
    return 0

def test_expenses_as_user():
    app.dependency_overrides[get_current_user] = fake_user
    response = client.get("/expenses")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == []
