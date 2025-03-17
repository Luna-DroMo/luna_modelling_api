from pydantic import BaseModel, field_validator
from typing import List, Any


class KalmanInput(BaseModel):
    results: List[List[float]]


class KalmanOutput(BaseModel):
    processed_results: List[float]
    input_data: List[List[float]]
