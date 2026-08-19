import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt

# ==========================================
# 1. Load Dataset
# ==========================================

DATASET = "WA_Fn-UseC_-Telco-Customer-Churn.csv"

df = pd.read_csv(DATASET)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# ==========================================
# 2. Data Cleaning
# ==========================================

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df["TotalCharges"] = df["TotalCharges"].fillna(
    df["TotalCharges"].median()
)

# Drop customer ID
if "customerID" in df.columns:
    df = df.drop(columns=["customerID"])

# ==========================================
# 3. Encode Target
# ==========================================

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

# ==========================================
# 4. Separate Features
# ==========================================

X = df.drop(columns=["Churn"])

# ==========================================
# 5. Load Label Encoders
# ==========================================

label_encoders = joblib.load(
    "label_encoders.pkl"
)

print("\nLabel encoders loaded successfully!")

# ==========================================
# 6. Apply Same Encoding
# ==========================================

for column, encoder in label_encoders.items():

    if column in X.columns:

        X[column] = X[column].astype(str)

        X[column] = encoder.transform(
            X[column]
        )

# ==========================================
# 7. Load XGBoost Model
# ==========================================

model = joblib.load(
    "xgboost_churn_model.pkl"
)

print("XGBoost model loaded successfully!")

# ==========================================
# 8. SHAP Explainer
# ==========================================

print("\nCreating SHAP explainer...")

explainer = shap.TreeExplainer(model)

# Calculate SHAP values
shap_values = explainer.shap_values(X)

print("SHAP values calculated successfully!")

# ==========================================
# 9. SHAP Summary Plot
# ==========================================

print("\nCreating SHAP summary plot...")

plt.figure()

shap.summary_plot(
    shap_values,
    X,
    show=False
)

plt.title(
    "SHAP Summary Plot - XGBoost Churn Model"
)

plt.tight_layout()

plt.savefig(
    "shap_summary_plot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved: shap_summary_plot.png"
)

# ==========================================
# 10. SHAP Bar Plot
# ==========================================

print("\nCreating SHAP feature importance plot...")

plt.figure()

shap.summary_plot(
    shap_values,
    X,
    plot_type="bar",
    show=False
)

plt.title(
    "SHAP Feature Importance - XGBoost"
)

plt.tight_layout()

plt.savefig(
    "shap_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Saved: shap_feature_importance.png"
)

# ==========================================
# 11. Calculate Mean Absolute SHAP
# ==========================================

mean_shap = np.abs(shap_values).mean(
    axis=0
)

shap_importance = pd.DataFrame({
    "Feature": X.columns,
    "Mean_SHAP_Value": mean_shap
})

shap_importance = shap_importance.sort_values(
    by="Mean_SHAP_Value",
    ascending=False
)

# ==========================================
# 12. Display Top Features
# ==========================================

print("\n========================================")
print("TOP 15 SHAP FEATURES")
print("========================================")

print(
    shap_importance
    .head(15)
    .to_string(index=False)
)

# ==========================================
# 13. Save SHAP Results
# ==========================================

shap_importance.to_csv(
    "shap_feature_importance.csv",
    index=False
)

print(
    "\nSaved: shap_feature_importance.csv"
)

# ==========================================
# 14. Final Message
# ==========================================

print("\n========================================")
print("SHAP ANALYSIS COMPLETED SUCCESSFULLY")
print("========================================")