# Week 2 - Day 2: Advanced Feature Engineering

## Objective

The objective of this task is to create advanced features from the Telco Customer Churn dataset that capture customer behavior, engagement levels, and service usage patterns. These engineered features help improve data quality and provide valuable inputs for predictive modeling.

---

## Dataset Used

- Dataset: WA_Fn-UseC_-Telco-Customer-Churn.csv
- Source: IBM Telco Customer Churn Dataset
- Records: 7043 Customers

---

## Features Created

### 1. Customer Engagement Level

A new feature was created using service adoption patterns to classify customers into engagement categories.

Categories:
- Low
- Medium
- High

Purpose:
- Understand customer involvement with company services.
- Identify customers with low engagement who may be at higher risk of churn.

---

### 2. Total Services

A new feature was created by counting the number of services subscribed by each customer.

Services considered:
- Phone Service
- Multiple Lines
- Internet Service
- Online Security
- Online Backup
- Device Protection
- Tech Support
- Streaming TV
- Streaming Movies

Purpose:
- Measure customer dependency on company services.
- Analyze customer value and retention behavior.

---

### 3. Internet Service Analysis

Internet service categories were analyzed to understand customer distribution.

Categories:
- DSL
- Fiber Optic
- No Internet Service

Purpose:
- Compare service adoption trends.
- Support churn analysis based on internet type.

---

## Visualizations Created

### Customer Engagement Level Distribution
Shows the number of customers in each engagement category.

### Churn vs Customer Engagement Level
Analyzes churn behavior across different engagement levels.

### Average Monthly Charges by Engagement Level
Compares average monthly charges among engagement groups.

### Total Services Distribution
Displays customer distribution based on the number of subscribed services.

### Internet Service Distribution
Shows the distribution of customers across internet service types.

---

## Output Files Generated

### Dataset
- telco_feature_engineered_commit2.csv

### Screenshots
- week2_commit2_dashboard.png


---

## Key Insights

- Customers with higher engagement generally subscribe to more services.
- Service adoption provides useful information about customer behavior.
- Internet service type significantly affects customer distribution.
- Engineered features provide stronger business insights than raw data alone.

---

## Conclusion

Advanced feature engineering was successfully performed on the Telco Customer Churn dataset. New features such as Customer Engagement Level and Total Services were created to better represent customer behavior and service usage patterns. Visual analysis highlighted relationships between engagement levels, service adoption, monthly charges, and churn behavior. The resulting feature-engineered dataset is more informative, business-oriented, and ready for predictive modeling in the next phase of the project.