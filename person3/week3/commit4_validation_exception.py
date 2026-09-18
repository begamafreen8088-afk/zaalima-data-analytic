from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
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

    @validator("tenure", "MonthlyCharges", "TotalCharges")
    def must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v

@app.post("/predict")
def predict_churn(customer: CustomerData):
    try:
        data = pd.DataFrame([customer.dict()])
        prediction = model.predict(data)[0]
        probability = model.predict_proba(data)[0][1]
        return {
            "churn_prediction": int(prediction),
            "churn_probability": round(float(probability), 4),
            "risk_level": "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return {"error": str(exc), "status": "failed"}
