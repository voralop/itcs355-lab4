import pytest
from fastapi.testclient import TestClient
from service.app import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_readiness_check(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_single_predict_success(client):
    response = client.post("/predict", json={"amount": 1500.0})
    assert response.status_code == 200
    data = response.json()
    assert "is_fraud" in data
    assert data["model_version"] == "v1.0.0"

def test_single_predict_validation_failure(client):
    response = client.post("/predict", json={"amount": -100.0})
    assert response.status_code == 422

def test_batch_predict_success(client):
    payload = {
        "items": [{"amount": 100.0}, {"amount": 2500.0}]
    }
    response = client.post("/predict/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["predictions"]) == 2
    assert data["model_version"] == "v1.0.0"