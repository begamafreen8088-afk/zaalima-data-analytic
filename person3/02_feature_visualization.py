import pandas as pd
import matplotlib.pyplot as plt

# Load final preprocessed dataset
file_path = "data/processed/telco_preprocessed_final.csv"
df = pd.read_csv(file_path)

print("========== FEATURE VISUALIZATION & INSIGHTS ==========")
print("Dataset Shape:", df.shape)

# -------------------------------
# 1. Churn Distribution
# -------------------------------

churn_counts = df["Churn"].value_counts()

plt.figure(figsize=(7, 5))
churn_counts.plot(kind="bar")

plt.title("Customer Churn Distribution")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Number of Customers")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig(
    "reports/churn_distribution.png",
    dpi=300
)
plt.close()


# -------------------------------
# 2. Tenure Distribution by Churn
# -------------------------------

plt.figure(figsize=(8, 5))

df.groupby("Churn")["tenure"].mean().plot(kind="bar")

plt.title("Average Tenure by Churn Status")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Average Tenure")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig(
    "reports/tenure_vs_churn.png",
    dpi=300
)
plt.close()


# -------------------------------
# 3. Monthly Charges by Churn
# -------------------------------

plt.figure(figsize=(8, 5))

df.groupby("Churn")["MonthlyCharges"].mean().plot(kind="bar")

plt.title("Average Monthly Charges by Churn Status")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Average Monthly Charges")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig(
    "reports/monthly_charges_vs_churn.png",
    dpi=300
)
plt.close()


# -------------------------------
# 4. Total Charges by Churn
# -------------------------------

plt.figure(figsize=(8, 5))

df.groupby("Churn")["TotalCharges"].mean().plot(kind="bar")

plt.title("Average Total Charges by Churn Status")
plt.xlabel("Churn (0 = No, 1 = Yes)")
plt.ylabel("Average Total Charges")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig(
    "reports/total_charges_vs_churn.png",
    dpi=300
)
plt.close()


# -------------------------------
# 5. Contract-related Features
# -------------------------------

contract_columns = [
    "Contract_One year",
    "Contract_Two year"
]

contract_means = df.groupby("Churn")[contract_columns].mean()

print("\n========== CONTRACT FEATURES ==========")
print(contract_means)


# -------------------------------
# 6. Service-related Features
# -------------------------------

service_columns = [
    "InternetService_Fiber optic",
    "InternetService_No",
    "OnlineSecurity_Yes",
    "OnlineBackup_Yes",
    "DeviceProtection_Yes",
    "TechSupport_Yes",
    "StreamingTV_Yes",
    "StreamingMovies_Yes"
]

service_means = df.groupby("Churn")[service_columns].mean()

print("\n========== SERVICE FEATURES ==========")
print(service_means)


# -------------------------------
# Final message
# -------------------------------

print("\n========== VISUALIZATION COMPLETED ==========")

print("Charts saved:")
print("reports/churn_distribution.png")
print("reports/tenure_vs_churn.png")
print("reports/monthly_charges_vs_churn.png")
print("reports/total_charges_vs_churn.png")