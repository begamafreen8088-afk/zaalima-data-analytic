import pandas as pd

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("===== DATASET INSPECTION =====")
print("\nShape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nColumn Data Types:")
print(df.dtypes)
print("\nMissing Values:")
print(df.isnull().sum())
print("\nInvalid TotalCharges (blank spaces):")
invalid = df[df["TotalCharges"].str.strip() == ""]
print(f"Count: {len(invalid)}")
print(invalid[["customerID", "tenure", "MonthlyCharges", "TotalCharges"]])
