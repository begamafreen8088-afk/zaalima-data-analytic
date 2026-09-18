import pandas as pd
import shap
import pickle
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/telco_preprocessed_final.csv")
X = df.drop("Churn", axis=1)

with open("data/models/xgboost_churn_model.pkl", "rb") as f:
    model = pickle.load(f)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# SHAP summary plot
shap.summary_plot(shap_values, X, show=False)
plt.tight_layout()
plt.savefig("Reports/week2/person3_shap_summary.png", dpi=150)
plt.close()

# SHAP feature importance bar plot
shap.summary_plot(shap_values, X, plot_type="bar", show=False)
plt.tight_layout()
plt.savefig("Reports/week2/person3_shap_feature_importance.png", dpi=150)
plt.close()

print("SHAP analysis complete.")
print("Top features by SHAP importance saved.")
