import pandas as pd

print("=" * 50)
print("TELCO CATEGORICAL FEATURE ENCODING")
print("=" * 50)

# Load cleaned dataset
INPUT_PATH = "data/processed/telco_cleaned.csv"
OUTPUT_PATH = "data/processed/telco_encoded.csv"

df = pd.read_csv(INPUT_PATH)

print("\nOriginal Shape:")
print(df.shape)

# Convert target variable Churn to numbers
df["Churn"] = df["Churn"].map({
    "Yes": 1,
    "No": 0
})

# Remove customerID because it is unique for every customer
df = df.drop(columns=["customerID"])

# Find categorical columns
categorical_columns = df.select_dtypes(
    include=["object"]
).columns.tolist()

print("\nCategorical Columns:")
print(categorical_columns)

# One-Hot Encoding
df_encoded = pd.get_dummies(
    df,
    columns=categorical_columns,
    drop_first=True,
    dtype=int
)

print("\nEncoded Shape:")
print(df_encoded.shape)

print("\nRemaining Object Columns:")
print(
    df_encoded.select_dtypes(
        include=["object"]
    ).columns.tolist()
)

print("\nTotal Missing Values:")
print(df_encoded.isnull().sum().sum())

# Save encoded dataset
df_encoded.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nEncoded dataset saved successfully!")
print(OUTPUT_PATH)