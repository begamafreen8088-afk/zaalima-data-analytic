import pandas as pd

# 1. Load cleaned dataset from Commit 2
file_path = "data/processed/telco_cleaned.csv"

df = pd.read_csv(file_path)

print("========== BEFORE ENCODING ==========")
print("Dataset Shape:", df.shape)

print("\nCategorical Columns:")
print(df.select_dtypes(include=["object"]).columns.tolist())


# 2. Binary categorical columns
binary_columns = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "PaperlessBilling",
    "Churn"
]

# Convert Yes/No and Male/Female values to 0/1
df["gender"] = df["gender"].map({
    "Female": 0,
    "Male": 1
})

for column in [
    "Partner",
    "Dependents",
    "PhoneService",
    "PaperlessBilling",
    "Churn"
]:
    df[column] = df[column].map({
        "No": 0,
        "Yes": 1
    })


# 3. Multi-category columns
categorical_columns = [
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaymentMethod"
]

# One-Hot Encoding
df = pd.get_dummies(
    df,
    columns=categorical_columns,
    drop_first=True,
    dtype=int
)


# 4. Remove customerID because it is an identifier
df = df.drop(columns=["customerID"])


# 5. Final verification
print("\n========== AFTER ENCODING ==========")

print("Dataset Shape:", df.shape)

print("\nRemaining Object Columns:")
print(df.select_dtypes(include=["object"]).columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nFirst 5 Rows:")
print(df.head())


# 6. Save encoded dataset
output_path = "data/processed/telco_encoded.csv"

df.to_csv(
    output_path,
    index=False
)

print("\nEncoded dataset saved successfully:")
print(output_path)