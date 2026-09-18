# Deployment Guide - Customer Churn Prediction API

## Person 3 - Renuka | Week 4: Deployment & Docker

---

## Prerequisites
- Docker & Docker Compose installed
- Python 3.10+
- Trained model file: `data/models/xgboost_churn_model.pkl`

---

## Quick Start

### 1. Build and Run with Docker Compose
```bash
docker-compose up --build
```

### 2. Access the API
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | API health check |
| `/predict` | POST | Single customer churn prediction |
| `/batch_predict` | POST | Batch prediction for multiple customers |

---

## Sample Request - /predict
```json
{
  "tenure": 24,
  "MonthlyCharges": 65.5,
  "TotalCharges": 1572.0,
  "Contract": 1,
  "InternetService": 1,
  "PaymentMethod": 2,
  "PaperlessBilling": 1,
  "OnlineSecurity": 0,
  "TechSupport": 0,
  "StreamingTV": 1,
  "StreamingMovies": 1,
  "gender": 1,
  "SeniorCitizen": 0,
  "Partner": 1,
  "Dependents": 0,
  "PhoneService": 1,
  "MultipleLines": 0,
  "OnlineBackup": 1,
  "DeviceProtection": 0
}
```

## Sample Response
```json
{
  "churn_prediction": 0,
  "churn_probability": 0.2341,
  "risk_level": "Low"
}
```

---

## Docker Commands

```bash
# Build image
docker build -t churn-api .

# Run container
docker run -p 8000:8000 churn-api

# Stop all services
docker-compose down

# View logs
docker-compose logs -f api
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | postgresql://admin:password@db:5432/churndb | PostgreSQL connection |
| `MODEL_PATH` | data/models/xgboost_churn_model.pkl | Model file path |

---

## Project Summary
- Model: XGBoost Classifier
- Accuracy: ~80%
- ROC-AUC: ~0.84
- Deployment: FastAPI + Docker + PostgreSQL
