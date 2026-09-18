import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/processed/telco_step1_cleaned.csv")

# Encode target variable
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# Label encode all categorical columns
le = LabelEncoder()
cat_cols = df.select_dtypes(include="object").columns.tolist()
cat_cols.remove("customerID")

for col in cat_cols:
    df[col] = le.fit_transform(df[col])

print("Encoding complete.")
print(df.head())
print("\nData types after encoding:")
print(df.dtypes)

df.to_csv("data/processed/telco_step2_encoded.csv", index=False)
print("\nEncoded dataset saved.")
