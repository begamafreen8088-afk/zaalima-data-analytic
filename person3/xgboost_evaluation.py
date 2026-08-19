import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# ==========================================
# 1. Load Dataset
# ==========================================

DATASET = "WA_Fn-UseC_-Telco-Customer-Churn.csv"

df = pd.read_csv(DATASET)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# ==========================================
# 2. Basic Cleaning
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
# 4. Separate X and y
# ==========================================

X = df.drop(columns=["Churn"])
y = df["Churn"]

# ==========================================
# 5. Load Label Encoders
# ==========================================

label_encoders = joblib.load("label_encoders.pkl")

print("\nLabel encoders loaded successfully!")

# ==========================================
# 6. Apply SAME Label Encoding
# ==========================================

for column, encoder in label_encoders.items():

    if column in X.columns:

        # Convert to string to avoid datatype issues
        X[column] = X[column].astype(str)

        X[column] = encoder.transform(
            X[column]
        )

# ==========================================
# 7. Train-Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# ==========================================
# 8. Load XGBoost Model
# ==========================================

model = joblib.load(
    "xgboost_churn_model.pkl"
)

print("\nXGBoost model loaded successfully!")

# ==========================================
# 9. Check Feature Names
# ==========================================

print("\nModel Features:")
print(model.get_booster().feature_names)

print("\nEvaluation Features:")
print(X_test.columns.tolist())

# ==========================================
# 10. Predictions
# ==========================================

y_pred = model.predict(X_test)

y_prob = model.predict_proba(
    X_test
)[:, 1]

# ==========================================
# 11. Metrics
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

# ==========================================
# 12. Print Evaluation
# ==========================================

print("\n========================================")
print("XGBOOST MODEL EVALUATION")
print("========================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")

# ==========================================
# 13. Classification Report
# ==========================================

print("\n========================================")
print("CLASSIFICATION REPORT")
print("========================================")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Not Churn",
            "Churn"
        ],
        zero_division=0
    )
)

# ==========================================
# 14. Confusion Matrix
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\n========================================")
print("CONFUSION MATRIX")
print("========================================")

print(cm)

print("\nTrue Negative :", cm[0][0])
print("False Positive:", cm[0][1])
print("False Negative:", cm[1][0])
print("True Positive :", cm[1][1])

# ==========================================
# 15. Feature Importance
# ==========================================

feature_importance = pd.DataFrame({
    "Feature": X_test.columns,
    "Importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n========================================")
print("TOP 10 FEATURES")
print("========================================")

print(
    feature_importance
    .head(10)
    .to_string(index=False)
)

# ==========================================
# 16. Save Evaluation Results
# ==========================================

results = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC"
    ],
    "Score": [
        accuracy,
        precision,
        recall,
        f1,
        roc_auc
    ]
})

results.to_csv(
    "xgboost_evaluation_results.csv",
    index=False
)

print("\nEvaluation results saved as:")
print("xgboost_evaluation_results.csv")

# ==========================================
# 17. Save Confusion Matrix
# ==========================================

cm_df = pd.DataFrame(
    cm,
    index=[
        "Actual Not Churn",
        "Actual Churn"
    ],
    columns=[
        "Predicted Not Churn",
        "Predicted Churn"
    ]
)

cm_df.to_csv(
    "xgboost_confusion_matrix.csv"
)

print("Confusion matrix saved as:")
print("xgboost_confusion_matrix.csv")

print("\n========================================")
print("XGBOOST EVALUATION COMPLETED SUCCESSFULLY")
print("========================================")