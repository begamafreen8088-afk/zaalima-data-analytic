import pandas as pd
import numpy as np

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

# LTV = MonthlyCharges * tenure
df["LTV"] = df["MonthlyCharges"] * df["tenure"]

print("LTV Statistics:")
print(df["LTV"].describe())

print("\nAverage LTV by Contract Type:")
print(df.groupby("Contract")["LTV"].mean().round(2))

df.to_csv("data/ltv_prepared_dataset.csv", index=False)
print("\nLTV dataset saved.")
