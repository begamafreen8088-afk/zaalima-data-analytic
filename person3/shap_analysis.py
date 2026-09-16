import pandas as pd
import shap
import pickle
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/telco_person3_week1_cleaned_encoded.csv")
X = df.drop("Churn", axis=1)

with open("data/models/person3_best_ltv_random_forest.pkl", "rb") as f:
    model = pickle.load(f)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

shap.summary_plot(shap_values[1], X, show=False)
plt.tight_layout()
plt.savefig("Reports/week2/person3_shap_summary.png", dpi=150)
plt.close()

print("SHAP summary plot saved.")
