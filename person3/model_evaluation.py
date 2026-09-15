import pandas as pd
import pickle
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/telco_person3_week1_cleaned_encoded.csv")
X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

with open("data/logistic_regression_model.pkl", "rb") as f:
    model = pickle.load(f)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

cm = confusion_matrix(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print("Confusion Matrix:")
print(cm)
print(f"ROC-AUC Score: {auc:.4f}")
