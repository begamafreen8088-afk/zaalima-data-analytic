import pandas as pd

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("Contract Distribution")
print(df["Contract"].value_counts())

print("\nChurn Distribution")
print(df["Churn"].value_counts())

print("\nAverage Tenure by Churn")
print(df.groupby("Churn")["tenure"].mean())

print("\nContract vs Churn")
print(pd.crosstab(df["Contract"], df["Churn"]))