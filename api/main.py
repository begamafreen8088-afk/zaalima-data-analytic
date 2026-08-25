from fastapi import FastAPI, HTTPException

from api.schemas import CustomerInput
from api.model_loader import load_model


app = FastAPI(
    title="Customer LTV Prediction API",
    description="API for predicting Customer Lifetime Value (LTV)",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Customer LTV Prediction API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict_ltv(customer: CustomerInput):

    try:
        # Load trained model
        model = load_model()

        # Prepare customer input
        input_data = [[
            customer.tenure,
            customer.monthly_charges,
            customer.total_charges
        ]]

        # Generate prediction
        prediction = model.predict(input_data)

        # Return prediction
        return {
            "predicted_ltv": round(
                float(prediction[0]),
                2
            )
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )