from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib

from api.model_loader import load_model
from api.schemas import (
    CustomerInput,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
)


# --------------------------------------------------
# Load Model
# --------------------------------------------------

try:
    model = load_model()
except Exception as e:
    model = None
    print(f"Model loading failed: {e}")


# --------------------------------------------------
# Load Label Encoders
# --------------------------------------------------

try:
    encoders = joblib.load("person3/label_encoders.pkl")
except Exception as e:
    encoders = None
    print(f"Encoder loading failed: {e}")


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="Customer Churn Prediction API",
    description="FastAPI API for single and batch customer churn prediction",
    version="1.0.0",
)


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Customer Churn Prediction API is running"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "encoders_loaded": encoders is not None,
    }


# --------------------------------------------------
# Prepare Customer Data
# --------------------------------------------------

def prepare_customer(customer: CustomerInput):

    data = {
        "gender": customer.gender,
        "SeniorCitizen": customer.SeniorCitizen,
        "Partner": customer.Partner,
        "Dependents": customer.Dependents,
        "tenure": customer.tenure,
        "PhoneService": customer.PhoneService,
        "MultipleLines": customer.MultipleLines,
        "InternetService": customer.InternetService,
        "OnlineSecurity": customer.OnlineSecurity,
        "OnlineBackup": customer.OnlineBackup,
        "DeviceProtection": customer.DeviceProtection,
        "TechSupport": customer.TechSupport,
        "StreamingTV": customer.StreamingTV,
        "StreamingMovies": customer.StreamingMovies,
        "Contract": customer.Contract,
        "PaperlessBilling": customer.PaperlessBilling,
        "PaymentMethod": customer.PaymentMethod,
        "MonthlyCharges": customer.MonthlyCharges,
        "TotalCharges": customer.TotalCharges,
    }

    df = pd.DataFrame([data])

    # Encode categorical columns
    categorical_columns = [
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
    ]

    if encoders is None:
        raise ValueError("Label encoders are not loaded")

    for column in categorical_columns:

        if column not in encoders:
            raise ValueError(
                f"Encoder not found for column: {column}"
            )

        encoder = encoders[column]

        try:
            df[column] = encoder.transform(df[column])
        except ValueError:
            raise ValueError(
                f"Invalid value '{df[column].iloc[0]}' "
                f"for column '{column}'. "
                f"Allowed values: {list(encoder.classes_)}"
            )

    return df


# --------------------------------------------------
# Single Customer Prediction
# --------------------------------------------------

@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: CustomerInput):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model is not loaded"
        )

    try:

        df = prepare_customer(request)

        prediction = model.predict(df)[0]

        probability = model.predict_proba(df)[0][1]

        return {
            "prediction": int(prediction),
            "probability": float(probability),
        }

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


# --------------------------------------------------
# Batch Prediction
# --------------------------------------------------

@app.post(
    "/batch_predict",
    response_model=BatchPredictionResponse
)
def batch_predict(request: BatchPredictionRequest):

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model is not loaded"
        )

    try:

        results = []

        for customer in request.customers:

            df = prepare_customer(customer)

            prediction = model.predict(df)[0]

            probability = model.predict_proba(df)[0][1]

            results.append({
                "prediction": int(prediction),
                "probability": float(probability),
            })

        return {
            "predictions": results
        }

    except ValueError as e:

        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )