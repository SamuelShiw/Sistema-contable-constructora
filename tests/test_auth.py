from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_admin_success() -> None:
    payload = {
        "email": "admin@constructora.com",
        "password": "admin123",
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials() -> None:
    payload = {
        "email": "admin@constructora.com",
        "password": "wrong-password",
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 401