# zaalima-data-analytic

## project -1

## Customer Churn Prediction & Lifetime Value (LTV) Engine

## Project Overview

Customer retention is one of the most important challenges faced by telecom and subscription-based businesses. This project aims to predict customer churn and estimate Customer Lifetime Value (LTV) using machine learning techniques. The system helps organizations identify customers at risk of leaving and prioritize high-value customers for retention campaigns.

## Problem Statement

Businesses lose revenue when customers discontinue their services. Acquiring new customers is often more expensive than retaining existing ones. This project addresses this problem by:

* Predicting customer churn.
* Estimating Customer Lifetime Value (LTV).
* Generating business insights for customer retention strategies.
* Supporting data-driven decision making.

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

## Week 4 – Business Intelligence, Churn Trends & Risk Intelligence Suite

### Day 1: Churn Trend Analysis & Executive Reporting
* Longitudinal tenure cohort survival analysis
* Contract structure & commitment risk evaluation
* Revenue-at-risk & monthly spend tier vulnerability
* Service ecosystem & protective stickiness buffers
* Payment channel & billing friction assessment
* 2x2 Value vs. Risk retention segmentation matrix
* Interactive standalone HTML retention trends dashboard (`Reports/churn_trends_dashboard.html`)

### Day 2: Predictive Churn Risk Dashboard & Retention Engine
* Individual customer-level churn risk probability scoring (7,043 accounts)
* Calibrated Churn Risk Tiers: Critical (≥70%), High (45–70%), Medium (25–45%), Low (<25%)
* Top hazard catalysts vs. protective retention moat quantification
* Monthly recurring revenue ($139.6k/mo) and multi-year LTV exposure analysis
* 2x2 Value vs. Risk retention action matrix (Immediate Intervention, Automated Nurture, Core VIP Protect, Low Maintenance)
* Interactive executive Churn Risk Dashboard (`Reports/churn_risk_dashboard.html`)
  - Live filterable customer risk explorer with pagination and CSV export
  - Real-time customer risk & LTV profiler simulator with dynamic SVG gauge
  - Portfolio retention campaign ROI simulator
  - Departmental SLA retention playbooks (Customer Success, Marketing, Billing)
* Comprehensive executive markdown report (`Reports/churn_risk_report.md`)

### Day 3: Advanced Customer Segmentation & Behavioral Intelligence
* Strategic behavioral RFM personas (Champions & VIP Loyalists, At-Risk High Rollers, Budget Anchors, Vulnerable Newcomers, Digital Streamers, Core Steady)
* Unsupervised K-Means clustering ($k=4$) validated via Elbow Curve and Silhouette Coefficients ($0.403$)
* 2D Principal Component Analysis (PCA) projection (91.1% explained variance) with cluster centroids
* 4x4 Lifecycle Cohort × Spend Tier cross-tabulation heatmaps (Volume, Churn %, Expected Loss $)
* Service ecosystem penetration and defensive retention moat analysis
* Strategic portfolio bubble matrix (Predicted LTV vs. Churn Hazard with 4 investment quadrants)
* Interactive executive Customer Segmentation Dashboard (`Reports/customer_segmentation_dashboard.html`)
  - Filterable live customer segment explorer with search, multi-factor filtering, and CSV export
  - Visual persona profiling, K-Means mathematical diagnostics, and service stickiness tables
  - Cross-dashboard navigation connecting Trends, Risk, and Segmentation suites
* Comprehensive executive markdown report (`Reports/customer_segmentation_report.md`)
* Milestone documentation (`docs/week4_day3_customer_segmentation.md`)

### Day 4: Executive Summary & Strategic Business Recommendations (Capstone)
* C-Suite Portfolio Health & Financial Risk Vital Signs ($456.1k/mo MRR, $139.6k/mo revenue at risk, 65.5% loss concentration)
* Machine Learning & Predictive Modeling Synthesis (ROC-AUC 0.846 churn classifier & R² 0.887 LTV regressor)
* Root-Cause Hazard Analysis (+36.1% Month-to-Month, +30.7% Lack of Security, +30.0% Onboarding cliff, +28.8% Electronic check)
* Five Actionable Strategic Business Recommendations:
  - Pillar 1: Concierge Retention Protocol for At-Risk High Rollers ($14.4k/mo saved, 493.6% ROI)
  - Pillar 2: 90-Day Digital Onboarding & Moat Engineering ($10.8k/mo saved, 506.3% ROI)
  - Pillar 3: Contract Commitment & Migration Architecture ($4.9k/mo saved, 217.8% ROI)
  - Pillar 4: Payment Modernization & Autopay Transition ($3.1k/mo saved, 163.8% ROI)
  - Pillar 5: Defensive Service Moat & Cyber-Shield Bundles ($1.6k/mo saved, 67.6% ROI)
* Multi-Scenario Financial Impact & ROI Model:
  - Conservative (15% reduction): $251.3k/yr preserved | +$182.4k/yr net profit | 264.8% ROI
  - Target (25% reduction): $418.9k/yr preserved | +$324.1k/yr net profit | 341.8% ROI
  - Aggressive (35% reduction): $586.4k/yr preserved | +$461.9k/yr net profit | 371.0% ROI
* Interactive C-Suite Executive Command Center Dashboard (`Reports/executive_summary_dashboard.html`)
  - Real-time dynamic ROI & retention budget simulator with interactive range controls
  - Five strategic pillar operational explorer with SLAs, playbooks, and departmental RACI
  - Unified 4-dashboard cross-navigation bar and print/boardroom PDF export mode
* Comprehensive C-Suite Master Report (`Reports/executive_summary_and_business_recommendations.md` & `Reports/business_recommendations_report.md`)
* Milestone documentation (`docs/week4_day4_executive_summary_recommendations.md`)

### Day 5: Validation of Dashboard Insights & Final Analytics Report (Production Sign-off)
* Automated End-to-End Test Suite (`scripts/validate_dashboard_insights.py`) asserting 108 data, statistical, financial, and UX tests (100% pass rate)
* Complete Data Reconciliation & Provenance Audit across 7,043 customer accounts (0 data leakage, 0 unhandled nulls)
* Statistical Calibration Proof (+0.35% variance between historical empirical loss and forward predictive expected loss)
* Risk Tier & Segment Loss Concentration verification (66.75% in Critical/High, 65.54% in High Rollers & Newcomers)
* Financial Model Sensitivity & Multi-Scenario Stress-Testing (Conservative 264.8%, Target 341.8%, Aggressive 371.0% ROI)
* Interactive Quality Assurance & Analytics Validation Cockpit (`Reports/analytics_validation_dashboard.html`)
  - Live metric lineage and data provenance explorer
  - Dynamic financial sensitivity and stress-test simulator
  - Automated unit & integration test runner console
  - Cross-functional engineering sign-off matrix (Afreen Begam, Srikanth Kondadasula, Renuka)
  - Unified 5-dashboard navigation bar across all suites
* Definitive Master Validation Report (`Reports/dashboard_insights_validation_report.md`)
* Milestone documentation (`docs/week4_day5_validation_dashboard_insights_final_report.md`)

## Machine Learning Models

Churn Prediction Models

1. Logistic Regression
2. Random Forest Classifier
3. XGBoost Classifier

LTV Prediction Models

1. Linear Regression
2. Random Forest Regressor
3. XGBoost Regressor


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

## Key Features

* Customer Churn Prediction
* Customer Lifetime Value Prediction
* Feature Engineering Pipeline
* Explainable AI using SHAP
* PostgreSQL Data Storage
* FastAPI Deployment Layer
* Business Insight Generation
* Scalable Production-Oriented Architecture
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

## Expected Business Impact

* Reduce customer churn.
* Improve customer retention strategies.
* Increase customer lifetime value.
* Optimize marketing campaign budgets.
* Enable data-driven business decisions.


## Future Enhancements

* Dashboard integration using Apache Superset or Metabase.
* Cloud deployment.
* Real-time prediction services.
* Automated model retraining pipeline.
* Advanced customer segmentation (✅ Completed - Week 4 Day 3).

## Project Status

✅ Week 1 Completed

✅ Week 2 Completed

✅ Week 3 Completed

✅ Week 4 Completed (BI Trends, Predictive Risk Engine, Customer Segmentation, Executive Recommendations & Capstone Validation QA)

Project: Customer Churn Prediction & Lifetime Value (LTV) Engine — Fully Validated & Production Certified
