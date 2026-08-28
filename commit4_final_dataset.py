import pandas as pd

# 1. Load encoded dataset
file_path = "data/processed/telco_encoded.csv"

df = pd.read_csv(file_path)

print("========== FINAL DATASET CHECK ==========")

# 2. Original dataset shape
print("Dataset Shape Before Duplicate Removal:", df.shape)


# 3. Check missing values
missing_values = df.isnull().sum().sum()

print("\nTotal Missing Values:", missing_values)


# 4. Check duplicate rows
duplicate_rows = df.duplicated().sum()

print("\nDuplicate Rows Before Removal:", duplicate_rows)


# 5. Remove duplicate rows
df = df.drop_duplicates().copy()


# 6. Verify duplicates after removal
duplicate_rows_after = df.duplicated().sum()

print("Duplicate Rows After Removal:", duplicate_rows_after)


# 7. Final dataset shape
print("\nFinal Dataset Shape:", df.shape)


# 8. Check data types
print("\nData Types:")
print(df.dtypes)


# 9. Check target variable
print("\nChurn Distribution:")
print(df["Churn"].value_counts())


# 10. Check target values
print("\nUnique Churn Values:")
print(df["Churn"].unique())


# 11. Final missing-value check
print("\nFinal Missing Values:")
print(df.isnull().sum().sum())


# 12. Display first 5 rows
print("\nFirst 5 Rows:")
print(df.head())


# 13. Save final preprocessed dataset
output_path = "data/processed/telco_preprocessed_final.csv"

df.to_csv(
    output_path,
    index=False
)

print("\nFinal preprocessed dataset saved successfully:")
print(output_path)