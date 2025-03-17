from pydantic import BaseModel
from typing import List


class KalmanInput(BaseModel):
    results: List[float]


class KalmanOutput(BaseModel):
    processed_results: List[float]
    input_data: List[float]
