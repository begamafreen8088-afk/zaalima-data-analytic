import pandas as pd
import matplotlib.pyplot as plt

# Load final preprocessed dataset
file_path = "data/processed/telco_preprocessed_final.csv"

df = pd.read_csv(file_path)

print("========== FEATURE CORRELATION ANALYSIS ==========")
print("Dataset Shape:", df.shape)

# Calculate correlation matrix
correlation_matrix = df.corr(numeric_only=True)

# Display correlation with Churn
print("\n========== CORRELATION WITH CHURN ==========")

churn_correlation = (
    correlation_matrix["Churn"]
    .sort_values(ascending=False)
)

print(churn_correlation)

# Save complete correlation matrix
correlation_matrix.to_csv(
    "reports/correlation_matrix.csv"
)

# Remove Churn itself for visualization
churn_features = (
    correlation_matrix["Churn"]
    .drop("Churn")
    .sort_values()
)

# Create visualization
plt.figure(figsize=(10, 8))

churn_features.plot(kind="barh")

plt.title("Feature Correlation with Churn")
plt.xlabel("Correlation")
plt.ylabel("Features")

plt.tight_layout()

# Save graph
plt.savefig(
    "reports/churn_feature_correlation.png",
    dpi=300
)

plt.show()

print("\nCorrelation analysis completed successfully.")
print("Correlation matrix saved to:")
print("reports/correlation_matrix.csv")

print("\nCorrelation graph saved to:")
print("reports/churn_feature_correlation.png")