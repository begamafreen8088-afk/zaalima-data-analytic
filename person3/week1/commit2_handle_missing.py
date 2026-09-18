import pandas as pd

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Fix TotalCharges - replace blank with NaN and convert
df["TotalCharges"] = df["TotalCharges"].replace(" ", float("nan"))
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Fill missing TotalCharges with median
df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

# Correct SeniorCitizen to object type for consistency
df["SeniorCitizen"] = df["SeniorCitizen"].map({0: "No", 1: "Yes"})

print("Missing values after fix:")
print(df.isnull().sum())
print("\nData types after fix:")
print(df.dtypes)

df.to_csv("data/processed/telco_step1_cleaned.csv", index=False)
print("\nCleaned dataset saved.")
