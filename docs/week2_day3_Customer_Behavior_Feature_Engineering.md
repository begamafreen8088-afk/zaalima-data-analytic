# Week 2 Day 3 - Customer Behavior Feature Engineering

## Objective

The objective of this task is to create customer behavior-based features that provide deeper insights into customer value, loyalty, and churn risk. These features help improve predictive modeling and customer segmentation.

---

## Dataset Used

- Dataset: WA_Fn-UseC_-Telco-Customer-Churn.csv
- Domain: Telecommunications Customer Churn Analysis
- Total Records: 7043 Customers

---

## Features Created

### 1. PremiumCustomerScore

Customers were classified as premium customers based on their monthly charges and service usage patterns.

Purpose:
- Identify customers contributing higher revenue.
- Support customer value segmentation.

---

### 2. HighValueCustomer

Customers with higher monthly charges and longer tenure were categorized as high-value customers.

Purpose:
- Identify loyal and profitable customers.
- Support retention strategies.

---

### 3. LongTermCustomer

Customers with tenure greater than or equal to 24 months were classified as long-term customers.

Purpose:
- Measure customer loyalty.
- Analyze retention trends.

---

### 4. ContractRiskLevel

Contract types were grouped into risk categories:

- High Risk → Month-to-Month
- Medium Risk → One Year
- Low Risk → Two Year

Purpose:
- Understand churn risk based on contract type.
- Support business decision-making.

---

### Dataset
- telco_feature_engineered_commit3.csv

---
## Key Insights

- Premium customers contribute significantly to business revenue.
- Long-term customers demonstrate higher loyalty and retention.
- Contract type plays a major role in determining churn risk.
- High-value customers can be targeted for personalized retention strategies.
- Customer behavior features provide meaningful business intelligence beyond raw customer data.

---

## Conclusion

Customer behavior-based feature engineering was successfully completed on the Telco Customer Churn dataset. New features including PremiumCustomerScore, HighValueCustomer, LongTermCustomer, and ContractRiskLevel were created to capture customer value, loyalty, and risk patterns. The dashboard visualizations provided meaningful insights into customer segments and contract-related behavior. These engineered features enhance the dataset and provide a stronger foundation for customer churn prediction and business decision-making in the next phase of the project.