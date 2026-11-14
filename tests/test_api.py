from fastapi.testclient import TestClient
from api import app

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


