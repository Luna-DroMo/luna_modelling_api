from pydantic import BaseModel, Field, field_validator
from typing import List


class PanasInput(BaseModel):
    """
    Input schema for PANAS (Positive and Negative Affect Schedule) form data.

    Expects an array of 20 Likert scale responses (1-5) in the order of the PANAS questionnaire.
    """
    results: List[float] = Field(...,
                                 description="Array of 20 Likert scale responses (1-5)")

    @field_validator('results')
    def validate_results_length(cls, v):
        if len(v) != 20:
            raise ValueError("PANAS form data must have exactly 20 items")
        return v

    @field_validator('results')
    def validate_results_range(cls, v):
        for item in v:
            if item < 1 or item > 5:
                raise ValueError("PANAS responses must be between 1 and 5")
        return v


class PanasOutput(BaseModel):
    """
    Output schema for PANAS processing results.

    Contains positive affect (PA) and negative affect (NA) scores.
    """
    positive_affect: float = Field(..., description="Positive Affect score")
    negative_affect: float = Field(..., description="Negative Affect score")
    input_data: List[float] = Field(..., description="Original input data")
