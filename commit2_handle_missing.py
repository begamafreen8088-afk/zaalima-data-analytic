import pandas as pd

# Load raw dataset
file_path = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"

df = pd.read_csv(file_path)

print("========== BEFORE CLEANING ==========")
print("Dataset Shape:", df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())


# Convert TotalCharges from object to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("\n========== AFTER TOTALCHARGES CONVERSION ==========")
print("TotalCharges Data Type:")
print(df["TotalCharges"].dtype)

print("\nMissing Values:")
print(df.isnull().sum())


# Remove rows where TotalCharges is missing
df = df.dropna(subset=["TotalCharges"]).copy()


# Final verification
print("\n========== AFTER CLEANING ==========")
print("Dataset Shape:", df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())
# Save cleaned dataset
output_path = "data/processed/telco_cleaned.csv"

df.to_csv(
    output_path,
    index=False
)

print("\nCleaned dataset saved successfully:")
print(output_path)