import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("=" * 50)
print("TELCO DATASET INSPECTION")
print("=" * 50)

print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. Column Names:")
print(df.columns.tolist())

print("\n3. Data Types:")
print(df.dtypes)

print("\n4. Missing Values:")
print(df.isnull().sum())

print("\n5. Duplicate Rows:")
print(df.duplicated().sum())

print("\n6. First 5 Rows:")
print(df.head())

print("\n7. Dataset Information:")
df.info()