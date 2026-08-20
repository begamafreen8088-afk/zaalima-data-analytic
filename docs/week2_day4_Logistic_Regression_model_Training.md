# Week 2 Day 4 - Logistic Regression Model Training

## Objective

To train a Logistic Regression model using the feature-engineered Telco Customer Churn dataset and predict customer churn.

## Dataset

- Dataset: `telco_feature_engineered_commit3.csv`
- Total records: 7,043
- Features: 33

## Data Preparation

- Converted `Churn` into a binary target:
  - `0` = No Churn
  - `1` = Churn
- Separated features (`X`) and target (`y`).
- Identified 21 categorical and 12 numerical features.
- Applied One-Hot Encoding to categorical features.
- Applied StandardScaler to numerical features.
- Split the data into 80% training and 20% testing sets.

## Model Training

A Logistic Regression model was trained using the preprocessed training data.

- Training records: 5,634
- Testing records: 1,409
- Processed features: 10,977
- Maximum iterations: 1000
- Random state: 42

## Prediction

The trained model generated predictions for 1,409 test customers.

## Model Accuracy

**Logistic Regression Accuracy: 79.49%**

## Classification Report

| Class | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| No Churn | 0.84 | 0.90 | 0.87 |
| Churn | 0.64 | 0.51 | 0.57 |

## Confusion Matrix

```text
[[929 106]
 [183 191]]

##  Conclusion

The Logistic Regression model was successfully trained and achieved an accuracy of 79.49%. The model performs better in identifying non-churn customers, while churn prediction can be further improved through model optimization and evaluation.