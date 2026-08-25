from pydantic import BaseModel, Field


class CustomerInput(BaseModel):
    tenure: int = Field(
        ...,
        ge=0,
        description="Customer tenure in months"
    )

    monthly_charges: float = Field(
        ...,
        ge=0,
        description="Customer monthly charges"
    )

    total_charges: float = Field(
        ...,
        ge=0,
        description="Customer total charges"
    )