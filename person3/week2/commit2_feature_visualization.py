import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/processed/telco_preprocessed_final.csv")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Tenure vs Churn
sns.boxplot(x="Churn", y="tenure", data=df, ax=axes[0][0])
axes[0][0].set_title("Tenure vs Churn")

# MonthlyCharges vs Churn
sns.boxplot(x="Churn", y="MonthlyCharges", data=df, ax=axes[0][1])
axes[0][1].set_title("Monthly Charges vs Churn")

# TotalCharges vs Churn
sns.boxplot(x="Churn", y="TotalCharges", data=df, ax=axes[1][0])
axes[1][0].set_title("Total Charges vs Churn")

# Contract vs Churn
df.groupby("Contract")["Churn"].mean().mul(100).plot(kind="bar", ax=axes[1][1], color="coral")
axes[1][1].set_title("Churn Rate by Contract Type (%)")
axes[1][1].set_ylabel("Churn Rate %")

plt.tight_layout()
plt.savefig("Reports/week2/person3_feature_visualization.png", dpi=150)
plt.close()
print("Feature visualization saved.")
