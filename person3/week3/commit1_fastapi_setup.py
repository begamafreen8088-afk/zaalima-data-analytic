from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn using trained ML model",
    version="1.0.0"
)

# Load model on startup
with open("data/models/xgboost_churn_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/")
def root():
    return {"message": "Churn Prediction API is running", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "ok", "model": "XGBoost Churn Classifier"}
