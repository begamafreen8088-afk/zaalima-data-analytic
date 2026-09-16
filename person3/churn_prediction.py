import pandas as pd
import pickle

def predict_churn(customer_data: dict) -> dict:
    with open("data/logistic_regression_model.pkl", "rb") as f:
        model = pickle.load(f)

    df = pd.DataFrame([customer_data])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 4),
        "risk_level": "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"
    }

if __name__ == "__main__":
    print("Churn prediction module ready.")
