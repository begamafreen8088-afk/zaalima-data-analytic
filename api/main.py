from fastapi import FastAPI

app = FastAPI(
    title="Customer Lifetime Value Prediction API",
    description="API for Customer Lifetime Value prediction",
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