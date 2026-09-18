import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("Health check passed:", response.json())

def test_predict():
    payload = {
        "tenure": 24, "MonthlyCharges": 65.5, "TotalCharges": 1572.0,
        "Contract": 1, "InternetService": 1, "PaymentMethod": 2,
        "PaperlessBilling": 1, "OnlineSecurity": 0, "TechSupport": 0,
        "StreamingTV": 1, "StreamingMovies": 1, "gender": 1,
        "SeniorCitizen": 0, "Partner": 1, "Dependents": 0,
        "PhoneService": 1, "MultipleLines": 0, "OnlineBackup": 1,
        "DeviceProtection": 0
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert "churn_prediction" in result
    assert "churn_probability" in result
    assert "risk_level" in result
    print("Predict endpoint passed:", result)

def test_batch_predict():
    payload = {"customers": [
        {"tenure": 24, "MonthlyCharges": 65.5, "TotalCharges": 1572.0,
         "Contract": 1, "InternetService": 1, "PaymentMethod": 2,
         "PaperlessBilling": 1, "OnlineSecurity": 0, "TechSupport": 0,
         "StreamingTV": 1, "StreamingMovies": 1, "gender": 1,
         "SeniorCitizen": 0, "Partner": 1, "Dependents": 0,
         "PhoneService": 1, "MultipleLines": 0, "OnlineBackup": 1,
         "DeviceProtection": 0}
    ]}
    response = requests.post(f"{BASE_URL}/batch_predict", json=payload)
    assert response.status_code == 200
    print("Batch predict endpoint passed:", response.json())

if __name__ == "__main__":
    test_health()
    test_predict()
    test_batch_predict()
    print("\nAll deployment tests passed!")
