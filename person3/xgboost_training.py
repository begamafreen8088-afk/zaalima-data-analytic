import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

from xgboost import XGBClassifier
import joblib


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================
# 2. REMOVE CUSTOMER ID
# ==========================================

df = df.drop("customerID", axis=1)


# ==========================================
# 3. CONVERT TOTALCHARGES TO NUMERIC
# ==========================================

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Remove rows with missing TotalCharges
df = df.dropna()


# ==========================================
# 4. ENCODE CATEGORICAL COLUMNS
# ==========================================

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

label_encoders = {}

for column in categorical_columns:

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(
        df[column]
    )

    label_encoders[column] = encoder


# ==========================================
# 5. DEFINE FEATURES AND TARGET
# ==========================================

X = df.drop("Churn", axis=1)

y = df["Churn"]


print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget:")
print("Churn")


# ==========================================
# 6. TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# ==========================================
# 7. CREATE XGBOOST MODEL
# ==========================================

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42
)


# ==========================================
# 8. TRAIN MODEL
# ==========================================

print("\nTraining XGBoost model...")

model.fit(
    X_train,
    y_train
)

print("XGBoost training completed!")


# ==========================================
# 9. PREDICTION
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 10. ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n========================================")
print("XGBOOST MODEL RESULTS")
print("========================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


# ==========================================
# 11. CLASSIFICATION REPORT
# ==========================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ==========================================
# 12. FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)


print("\nFeature Importance:")
print(importance)


# ==========================================
# 13. SAVE FEATURE IMPORTANCE
# ==========================================

importance.to_csv(
    "xgboost_feature_importance.csv",
    index=False
)

print(
    "\nFeature importance saved as:"
)

print(
    "xgboost_feature_importance.csv"
)


# ==========================================
# 14. SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "xgboost_churn_model.pkl"
)

print(
    "\nModel saved as:"
)

print(
    "xgboost_churn_model.pkl"
)


# ==========================================
# 15. SAVE ENCODERS
# ==========================================

joblib.dump(
    label_encoders,
    "label_encoders.pkl"
)

print(
    "\nEncoders saved as:"
)

print(
    "label_encoders.pkl"
)


# ==========================================
# FINAL
# ==========================================

print("\n========================================")
print("XGBOOST TRAINING COMPLETED SUCCESSFULLY")
print("========================================")