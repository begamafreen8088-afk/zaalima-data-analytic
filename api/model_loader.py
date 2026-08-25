import joblib
from pathlib import Path


MODEL_PATH = Path("models/best_ltv_model.pkl")


def load_model():
    """
    Load the trained LTV regression model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    return model