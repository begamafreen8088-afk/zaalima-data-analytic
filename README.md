# zaalima-data-analytic

## project -1

## Customer Churn Prediction & Lifetime Value (LTV) Engine

## Project Overview

Customer retention is one of the most important challenges faced by telecom and subscription-based businesses. This project aims to predict customer churn and estimate Customer Lifetime Value (LTV) using machine learning techniques. The system helps organizations identify customers at risk of leaving and prioritize high-value customers for retention campaigns.

⸻

## Problem Statement

Businesses lose revenue when customers discontinue their services. Acquiring new customers is often more expensive than retaining existing ones. This project addresses this problem by:

* Predicting customer churn.
* Estimating Customer Lifetime Value (LTV).
* Generating business insights for customer retention strategies.
* Supporting data-driven decision making.

⸻

## Dataset Information

Dataset: Telco Customer Churn Dataset

Source: Kaggle / IBM Watson Analytics

## Dataset Features:

* Customer demographics
* Contract information
* Internet service details
* Monthly charges
* Total charges
* Tenure
* Churn status

Total Records: 7000+ customers

⸻

## Technology Stack

### Database

* PostgreSQL
* SQLAlchemy

### Data Analysis & Processing

* Python
* Pandas
* NumPy

### Visualization

* Matplotlib
* Seaborn

### Machine Learning

* Scikit-Learn
* XGBoost
* SHAP

### API Development

* FastAPI

## Dashboarding

* Apache Superset / Metabase

⸻

## Project Architecture

Dataset

↓

PostgreSQL Database

↓

Data Cleaning & Preprocessing

↓

Feature Engineering

↓

Churn Prediction Models

(Logistic Regression, Random Forest, XGBoost)

↓

LTV Prediction Models

(Linear Regression, Random Forest Regressor, XGBoost Regressor)

↓

FastAPI Prediction Service

↓

Business Insights & Dashboard

⸻

## Week-wise Project Progress

## Week 1 – Data Engineering & Analytics Foundation

### PostgreSQL & Data Ingestion

* PostgreSQL database setup
* Database configuration
* Customer schema creation
* Telco dataset loading
* Data validation using SQL queries
* SQLAlchemy integration

### Exploratory Data Analysis (EDA)

* Customer demographic analysis
* Service feature analysis
* Contract and churn analysis
* Monthly charges analysis
* Correlation analysis
* Data visualization

### Data Cleaning & Preprocessing

* Missing value handling
* Data type corrections
* Categorical encoding
* Clean dataset creation
* Baseline churn analytics

⸻

## Week 2 – Churn Prediction Modeling

### Feature Engineering

* Tenure-based features
* Monthly charge features
* Service-based features
* Feature correlation analysis
* Data transformations

### Machine Learning Models

* Logistic Regression
* Random Forest Classifier
* XGBoost Classifier

### Model Evaluation

* Accuracy analysis
* Precision
* Recall
* F1 Score
* Feature Importance Analysis
* SHAP Explainability

⸻

## Week 3 – LTV Prediction & API Development

### LTV Regression Models

* Linear Regression
* Random Forest Regressor
* XGBoost Regressor

### Regression Evaluation Metrics

* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)
* R² Score

### FastAPI Development

* Project setup
* Single customer prediction endpoint
* Batch prediction endpoint
* Validation and exception handling
* Swagger API documentation
* Model integration

⸻

## Machine Learning Models

Churn Prediction Models

1. Logistic Regression
2. Random Forest Classifier
3. XGBoost Classifier

LTV Prediction Models

1. Linear Regression
2. Random Forest Regressor
3. XGBoost Regressor

⸻

## Evaluation Metrics

Classification Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

Regression Metrics

* MAE
* RMSE
* R² Score

⸻

## API Endpoints

Predict Single Customer

POST /predict

Predicts:

* Churn Probability
* Churn Status
* Customer Lifetime Value

Batch Prediction

POST /batch_predict

Predicts:

* Churn and LTV for multiple customers simultaneously

⸻

## Key Features

* Customer Churn Prediction
* Customer Lifetime Value Prediction
* Feature Engineering Pipeline
* Explainable AI using SHAP
* PostgreSQL Data Storage
* FastAPI Deployment Layer
* Business Insight Generation
* Scalable Production-Oriented Architecture

⸻

## Team Members & Contributions

### Afreen Begam
GitHub: https://github.com/begamafreen8088-afk

Responsibilities:
- PostgreSQL Database Setup
- Data Ingestion
- Feature Engineering
- Logistic Regression Modeling
- LTV Regression Modeling

### Srikanth kondadasula
GitHub: https://github.com/srikanthkondadasula2002-art

Responsibilities:
- Exploratory Data Analysis (EDA)
- Data Visualization
- Random Forest Modeling
- LTV Analysis
- Business Insights Generation

### Renuka
GitHub: https://github.com/renukadevi-kr

Responsibilities:
- Data Cleaning & Preprocessing
- XGBoost Modeling
- SHAP Explainability Analysis
- FastAPI Development
- API Integration
⸻

## Expected Business Impact

* Reduce customer churn.
* Improve customer retention strategies.
* Increase customer lifetime value.
* Optimize marketing campaign budgets.
* Enable data-driven business decisions.

⸻

## Future Enhancements

* Dashboard integration using Apache Superset or Metabase.
* Cloud deployment.
* Real-time prediction services.
* Automated model retraining pipeline.
* Advanced customer segmentation.

⸻

## Project Status

✅ Week 1 Completed

✅ Week 2 Completed

✅ Week 3 Completed

🚧 Week 4 In Progress

⸻ 

Project: Customer Churn Prediction & Lifetime Value (LTV) Engine
