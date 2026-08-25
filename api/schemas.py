from typing import List
from pydantic import BaseModel


# --------------------------------------------------
# Single Customer Input
# --------------------------------------------------

class CustomerInput(BaseModel):

    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


# --------------------------------------------------
# Single Prediction Response
# --------------------------------------------------

class PredictionResponse(BaseModel):

    prediction: int
    probability: float


# --------------------------------------------------
# Batch Prediction Request
# --------------------------------------------------

class BatchPredictionRequest(BaseModel):

    customers: List[CustomerInput]


# --------------------------------------------------
# Batch Prediction Response
# --------------------------------------------------

class BatchPredictionResponse(BaseModel):

    predictions: List[PredictionResponse]