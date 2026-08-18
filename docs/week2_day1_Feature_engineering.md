# Week 2 - Day 1: Tenure-Based Feature Engineering

## Objective
The objective of this task was to create new tenure-based features that can improve customer churn prediction performance.

## Dataset
Telco Customer Churn Dataset

## Features Engineered

### 1. Tenure Group
Customers were categorized into tenure ranges:

- Low (0–12 months)
- Medium (13–48 months)
- High (49+ months)

This feature helps identify customer loyalty levels.

### 2. Monthly Charge Category
Monthly charges were grouped into:

- Low
- Medium
- High

This feature helps analyze customer spending behavior.

## Implementation Steps

1. Loaded the Telco Customer Churn dataset.
2. Created tenure-based categories using customer tenure values.
3. Created monthly charge categories using MonthlyCharges.
4. Generated visualizations for feature distributions.
5. Saved the engineered dataset for future modeling tasks.

## Output Files

- `scripts/feature_engineering.ipynb`
- `data/telco_feature_engineered_commit1.csv`
- `screenshots/week2_commit1_tenure_group_distribution.png`
- `screenshots/week2_commit1_monthly_charge_distribution.png`

## Results

The newly engineered features successfully grouped customers into meaningful categories based on service duration and spending behavior.

## Conclusion

Tenure-based and monthly charge-based features were successfully engineered and added to the dataset. These features provide additional customer behavior insights and will be used in later stages of churn prediction model development.