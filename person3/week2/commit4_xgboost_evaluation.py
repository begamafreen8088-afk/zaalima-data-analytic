import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/processed/telco_preprocessed_final.csv")
X = df.drop("Churn", axis=1)
y = df["Churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load XGBoost
with open("data/models/xgboost_churn_model.pkl", "rb") as f:
    xgb = pickle.load(f)

# Compare models
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "XGBoost": xgb
}

results = []
for name, model in models.items():
    if name != "XGBoost":
        model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    results.append({
        "Model": name,
        "Accuracy": round(accuracy_score(y_test, y_pred), 4),
        "ROC_AUC": round(roc_auc_score(y_test, y_prob), 4)
    })

results_df = pd.DataFrame(results)
print(results_df)
results_df.to_csv("Reports/week2/person3_xgboost_model_results.csv", index=False)

# Confusion matrix for XGBoost
cm = confusion_matrix(y_test, xgb.predict(X_test))
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("XGBoost Confusion Matrix")
plt.tight_layout()
plt.savefig("Reports/week2/person3_xgboost_confusion_matrix.png", dpi=150)
plt.close()
print("Evaluation complete and saved.")
