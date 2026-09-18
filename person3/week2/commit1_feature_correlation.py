import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/processed/telco_preprocessed_final.csv")

print("===== FEATURE CORRELATION ANALYSIS =====")

# Correlation matrix
corr = df.corr()

# Top features correlated with Churn
churn_corr = corr["Churn"].drop("Churn").sort_values(ascending=False)
print("\nTop features correlated with Churn:")
print(churn_corr)

# Heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(corr, annot=False, cmap="coolwarm", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("Reports/week2/person3_feature_correlation_heatmap.png", dpi=150)
plt.close()
print("\nCorrelation heatmap saved.")
