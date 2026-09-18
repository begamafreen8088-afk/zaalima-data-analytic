import pandas as pd

df = pd.read_csv("data/processed/telco_step2_encoded.csv")

# Drop customerID - not needed for ML
df.drop("customerID", axis=1, inplace=True)

# Verify no nulls
assert df.isnull().sum().sum() == 0, "There are still missing values!"

print("Final preprocessed dataset:")
print(df.shape)
print(df.head())
print("\nAll columns:", df.columns.tolist())

df.to_csv("data/processed/telco_preprocessed_final.csv", index=False)
print("\nFinal preprocessed dataset saved.")
