import pandas as pd

# Load raw dataset
df = pd.read_csv(
    "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

print("=" * 50)
print("TELCO DATA CLEANING")
print("=" * 50)

print("\nOriginal Shape:")
print(df.shape)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Check TotalCharges before conversion
print("\nTotalCharges datatype BEFORE:")
print(df["TotalCharges"].dtype)

# Convert TotalCharges to numeric
# Invalid/blank values will become NaN
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("\nMissing values AFTER TotalCharges conversion:")
print(df["TotalCharges"].isnull().sum())

# Remove rows with invalid TotalCharges
df = df.dropna(subset=["TotalCharges"])

# Remove duplicate rows
df = df.drop_duplicates()

# Remove extra spaces from text columns
object_columns = df.select_dtypes(
    include="object"
).columns

for column in object_columns:
    df[column] = df[column].str.strip()

print("\nTotalCharges datatype AFTER:")
print(df["TotalCharges"].dtype)

print("\nFinal Shape:")
print(df.shape)

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Save cleaned dataset
OUTPUT_PATH = "data/processed/telco_cleaned.csv"

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nCleaned dataset saved successfully!")
print(OUTPUT_PATH)