import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Churn distribution
df["Churn"].value_counts().plot(kind="bar", ax=axes[0][0], color=["steelblue","tomato"])
axes[0][0].set_title("Churn Distribution")

# Tenure vs Churn
df.groupby("Churn")["tenure"].mean().plot(kind="bar", ax=axes[0][1], color=["steelblue","tomato"])
axes[0][1].set_title("Avg Tenure by Churn")

# Monthly Charges vs Churn
df.groupby("Churn")["MonthlyCharges"].mean().plot(kind="bar", ax=axes[1][0], color=["steelblue","tomato"])
axes[1][0].set_title("Avg Monthly Charges by Churn")

# Contract vs Churn
df.groupby("Contract")["Churn"].mean().mul(100).plot(kind="bar", ax=axes[1][1], color="coral")
axes[1][1].set_title("Churn Rate by Contract Type (%)")

plt.tight_layout()
plt.savefig("Reports/week4/person3_churn_overview_dashboard.png", dpi=150)
print("Dashboard saved.")
