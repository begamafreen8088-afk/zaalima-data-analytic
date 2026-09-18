from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List
import pickle
import pandas as pd
import uvicorn

app = FastAPI(
    title="Customer Churn Prediction API",
    description="""
    ## Churn Prediction API
    Predict whether a customer will churn based on their profile.
    - **/predict** - Single customer prediction
    - **/batch_predict** - Batch prediction for multiple customers
    - **/health** - API health check
    """,
    version="1.0.0",
    contact={"name": "Person 3 - Renuka", "email": "renuka@zaalima.com"}
)

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

    class Config:
        schema_extra = {
            "example": {
                "tenure": 24, "MonthlyCharges": 65.5, "TotalCharges": 1572.0,
                "Contract": 1, "InternetService": 1, "PaymentMethod": 2,
                "PaperlessBilling": 1, "OnlineSecurity": 0, "TechSupport": 0,
                "StreamingTV": 1, "StreamingMovies": 1, "gender": 1,
                "SeniorCitizen": 0, "Partner": 1, "Dependents": 0,
                "PhoneService": 1, "MultipleLines": 0, "OnlineBackup": 1,
                "DeviceProtection": 0
            }
        }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "model": "XGBoost Churn Classifier v1.0"}

@app.post("/predict", tags=["Prediction"])
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

if __name__ == "__main__":
    uvicorn.run("commit5_model_integration:app", host="0.0.0.0", port=8000, reload=True)
