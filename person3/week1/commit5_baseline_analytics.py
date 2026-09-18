import pandas as pd

df = pd.read_csv("data/processed/telco_preprocessed_final.csv")

print("===== BASELINE ANALYTICS =====")

# Churn rate
churn_rate = df["Churn"].mean() * 100
retention_rate = 100 - churn_rate
print(f"\nChurn Rate: {churn_rate:.2f}%")
print(f"Retention Rate: {retention_rate:.2f}%")
print(f"Total Customers: {len(df)}")
print(f"Churned: {int(df['Churn'].sum())}")
print(f"Retained: {int((df['Churn'] == 0).sum())}")

# Customer segments by tenure
def tenure_segment(tenure):
    if tenure <= 12:
        return "New Customer"
    elif tenure <= 36:
        return "Medium Tenure"
    else:
        return "Long Tenure"

df["TenureSegment"] = df["tenure"].apply(tenure_segment)
print("\n===== CUSTOMER SEGMENTS =====")
print(df["TenureSegment"].value_counts())

# Churn rate by segment
print("\nChurn Rate by Segment:")
print(df.groupby("TenureSegment")["Churn"].mean().mul(100).round(2))

# Basic statistics
print("\n===== BASIC STATISTICS =====")
print(df[["tenure", "MonthlyCharges", "TotalCharges"]].describe())

# Baseline model - majority class
majority_class = df["Churn"].mode()[0]
baseline_accuracy = (df["Churn"] == majority_class).mean() * 100
print(f"\nBaseline Accuracy (majority class): {baseline_accuracy:.2f}%")

# Save results
results = {
    "total_customers": len(df),
    "churned": int(df["Churn"].sum()),
    "retained": int((df["Churn"] == 0).sum()),
    "churn_rate_percent": round(churn_rate, 2),
    "retention_rate_percent": round(retention_rate, 2),
    "baseline_accuracy_percent": round(baseline_accuracy, 2)
}
pd.DataFrame([results]).to_csv("data/processed/baseline_analytics.csv", index=False)
print("\nBaseline analytics saved.")
