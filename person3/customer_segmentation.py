import pandas as pd

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

def segment_customer(row):
    if row["tenure"] <= 12:
        return "New"
    elif row["tenure"] <= 36:
        return "Growing"
    elif row["MonthlyCharges"] > 70:
        return "Premium"
    else:
        return "Loyal"

df["Segment"] = df.apply(segment_customer, axis=1)

print("Customer Segments:")
print(df["Segment"].value_counts())

print("\nChurn Rate by Segment:")
print(df.groupby("Segment")["Churn"].mean().mul(100).round(2))

df.to_csv("data/processed/telco_person3_week1_cleaned_encoded.csv", index=False)
print("\nSegmented dataset saved.")
