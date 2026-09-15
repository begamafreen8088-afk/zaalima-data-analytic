import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import pickle

df = pd.read_csv("data/processed/telco_person3_week1_cleaned_encoded.csv")
X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

xgb = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5,
                    use_label_encoder=False, eval_metric="logloss", random_state=42)
xgb.fit(X_train, y_train)

y_pred = xgb.predict(X_test)
y_prob = xgb.predict_proba(X_test)[:, 1]

print(f"XGBoost Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")

with open("data/models/xgboost_churn_model.pkl", "wb") as f:
    pickle.dump(xgb, f)

print("XGBoost model saved.")
