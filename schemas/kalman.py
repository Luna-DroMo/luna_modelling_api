from pydantic import BaseModel, Field
from typing import List, Any


class KalmanInput(BaseModel):
    results: List[List[float]] = Field(
        description="A 2D array with exactly one inner list containing time series values. "
                    "Example: [[10.2, 10.5, 10.1, 9.8, 10.3]]"
    )


class KalmanOutput(BaseModel):
    processed_results: List[float]
    input_data: List[List[float]]
