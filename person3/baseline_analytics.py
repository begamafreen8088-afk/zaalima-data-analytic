import pandas as pd

df = pd.read_csv("data/processed/telco_person3_week1_cleaned_encoded.csv")

churn_rate = df["Churn"].mean() * 100
retention_rate = 100 - churn_rate

print(f"Churn Rate: {churn_rate:.2f}%")
print(f"Retention Rate: {retention_rate:.2f}%")
print(f"Total Customers: {len(df)}")
print(f"Churned: {df['Churn'].sum()}")
