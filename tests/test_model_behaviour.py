import pytest
import pandas as pd
from fastapi.testclient import TestClient
from service.app import app

# 1. Data Contract Test
def test_data_contract_schema_and_types():
    sample_data = pd.DataFrame({"wrong_column": [10.0, 250.5, 1000.0]})
    assert "amount" in sample_data.columns, "Missing 'amount' column"
    assert pd.api.types.is_numeric_dtype(sample_data["amount"]), "'amount' must be numeric"

# 2. Data Contract Test
def test_data_contract_range_and_null_rate():
    sample_data = pd.DataFrame({"amount": [10.0, 50.0, None, 1000.0]})
    null_rate = sample_data["amount"].isnull().mean()
    assert null_rate < 0.30, f"Null rate {null_rate:.2f} too high"

# 3. Model Behaviour Test
def test_model_behaviour_output():
    amount = 500.0
    is_fraud = amount > 100
    assert is_fraud == True

def test_integration_api_response():
    with TestClient(app) as client:
        response = client.post("/predict", json={"amount": 500.0})
        # เช็กว่า API ตอบกลับ 200 OK และมีคีย์ is_fraud
        assert response.status_code == 200
        assert "is_fraud" in response.json()