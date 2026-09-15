import pandas as pd

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

report = {
    "total_customers": len(df),
    "churned": int(df["Churn"].sum()),
    "retained": int((df["Churn"] == 0).sum()),
    "churn_rate": round(df["Churn"].mean() * 100, 2),
    "avg_monthly_charges_churned": round(df[df["Churn"]==1]["MonthlyCharges"].mean(), 2),
    "avg_tenure_churned": round(df[df["Churn"]==1]["tenure"].mean(), 2),
}

report_df = pd.DataFrame([report])
report_df.to_csv("Reports/week4/person3_week4_business_summary.csv", index=False)

print("Churn Report:")
for k, v in report.items():
    print(f"  {k}: {v}")
print("\nReport saved.")
