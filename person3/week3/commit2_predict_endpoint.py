from fastapi import FastAPI
from pydantic import BaseModel
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

@app.post("/predict")
def predict_churn(customer: CustomerData):
    data = pd.DataFrame([customer.dict()])
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]
    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 4),
        "risk_level": "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
    }
