import pandas as pd

# 1. Load final preprocessed dataset
file_path = "data/processed/telco_preprocessed_final.csv"

df = pd.read_csv(file_path)

print("========== BASELINE ANALYTICS ==========")

# 2. Dataset overview
print("\nDataset Shape:")
print(df.shape)

print("\nTotal Customers:")
print(len(df))


# 3. Churn count
churn_counts = df["Churn"].value_counts()

print("\n========== CHURN COUNT ==========")
print(churn_counts)


# 4. Churn percentage
churn_rate = df["Churn"].mean() * 100

print("\nOverall Churn Rate:")
print(f"{churn_rate:.2f}%")


# 5. Retention percentage
retention_rate = (1 - df["Churn"].mean()) * 100

print("\nOverall Retention Rate:")
print(f"{retention_rate:.2f}%")


# 6. Customer segments based on tenure
def tenure_segment(tenure):
    if tenure <= 12:
        return "New Customer"
    elif tenure <= 36:
        return "Medium Tenure"
    else:
        return "Long Tenure"


df["TenureSegment"] = df["tenure"].apply(tenure_segment)

print("\n========== CUSTOMER SEGMENTS ==========")
print(df["TenureSegment"].value_counts())


# 7. Churn rate by customer segment
segment_churn = (
    df.groupby("TenureSegment")["Churn"]
    .mean()
    .mul(100)
    .round(2)
)

print("\nChurn Rate by Customer Segment:")
print(segment_churn)


# 8. Basic statistics
print("\n========== BASIC STATISTICS ==========")

print("\nTenure Statistics:")
print(df["tenure"].describe())

print("\nMonthly Charges Statistics:")
print(df["MonthlyCharges"].describe())

print("\nTotal Charges Statistics:")
print(df["TotalCharges"].describe())


# 9. Baseline prediction
# Predict the majority class for every customer
majority_class = df["Churn"].mode()[0]

baseline_predictions = [majority_class] * len(df)

baseline_accuracy = (
    df["Churn"] == baseline_predictions
).mean() * 100

print("\n========== BASELINE MODEL METRIC ==========")

print("Majority Class:", majority_class)
print(f"Baseline Accuracy: {baseline_accuracy:.2f}%")


# 10. Save baseline analytics results
results = {
    "total_customers": len(df),
    "churned_customers": int(df["Churn"].sum()),
    "non_churned_customers": int((df["Churn"] == 0).sum()),
    "churn_rate_percent": round(churn_rate, 2),
    "retention_rate_percent": round(retention_rate, 2),
    "baseline_majority_class": int(majority_class),
    "baseline_accuracy_percent": round(baseline_accuracy, 2)
}

results_df = pd.DataFrame([results])

output_path = "data/processed/baseline_analytics.csv"

results_df.to_csv(
    output_path,
    index=False
)

print("\nBaseline analytics saved successfully:")
print(output_path)