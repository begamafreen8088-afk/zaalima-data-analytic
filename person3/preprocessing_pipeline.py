import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocess(filepath: str, output_path: str):
    df = pd.read_csv(filepath)

    # Drop customerID
    df.drop("customerID", axis=1, inplace=True)

    # Fix TotalCharges
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

    # Encode target
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # Encode categorical columns
    le = LabelEncoder()
    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        df[col] = le.fit_transform(df[col])

    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")
    return df

if __name__ == "__main__":
    preprocess(
        "data/WA_Fn-UseC_-Telco-Customer-Churn.csv",
        "data/processed/telco_person3_week1_cleaned_encoded.csv"
    )
