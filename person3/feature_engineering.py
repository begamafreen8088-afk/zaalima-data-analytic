import pandas as pd

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Tenure groups
df["tenure_group"] = pd.cut(df["tenure"], bins=[0,12,24,48,60,72], labels=["0-12","12-24","24-48","48-60","60-72"])

# Monthly charges group
df["charges_group"] = pd.cut(df["MonthlyCharges"], bins=[0,30,60,90,120], labels=["Low","Medium","High","Very High"])

# Total services count
service_cols = ["PhoneService","MultipleLines","InternetService","OnlineSecurity",
                "OnlineBackup","DeviceProtection","TechSupport","StreamingTV","StreamingMovies"]
df["total_services"] = (df[service_cols] == "Yes").sum(axis=1)

df.to_csv("data/telco_feature_engineered_commit1.csv", index=False)
print("Feature engineering complete.")
print(df[["tenure_group","charges_group","total_services"]].head())
