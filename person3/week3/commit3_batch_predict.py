from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pickle
import pandas as pd

app = FastAPI(title="Churn Prediction API", version="1.0.0")

with open("data/models/xgboost_churn_model.pkl", "rb") as f:
    model = pickle.load(f)

class CustomerData(BaseModel):
    tenure: float
    MonthlyCharges: float
    TotalCharges: float
    Contract: int
    InternetService: int
    PaymentMethod: int
    PaperlessBilling: int
    OnlineSecurity: int
    TechSupport: int
    StreamingTV: int
    StreamingMovies: int
    gender: int
    SeniorCitizen: int
    Partner: int
    Dependents: int
    PhoneService: int
    MultipleLines: int
    OnlineBackup: int
    DeviceProtection: int

class BatchRequest(BaseModel):
    customers: List[CustomerData]

@app.post("/batch_predict")
def batch_predict(request: BatchRequest):
    data = pd.DataFrame([c.dict() for c in request.customers])
    predictions = model.predict(data)
    probabilities = model.predict_proba(data)[:, 1]
    results = []
    for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
        results.append({
            "customer_index": i,
            "churn_prediction": int(pred),
            "churn_probability": round(float(prob), 4),
            "risk_level": "High" if prob > 0.7 else "Medium" if prob > 0.4 else "Low"
        })
    return {"total": len(results), "predictions": results}
