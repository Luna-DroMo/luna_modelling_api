from pydantic import BaseModel, field_validator, Field
from typing import List, Any


class KalmanInput(BaseModel):
    results: List[List[float]] = Field(
        description="A 2D array where each inner list contains time series values. "
                    "Example: [[10.2, 10.5, 10.1, 9.8, 10.3]]"
    )
    save: bool = Field(
        default=False,
        description="Whether to save the results to the database"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "results": [[10.2, 10.5, 10.1, 9.8, 10.3]],
                "save": False
            }
        }


class KalmanOutput(BaseModel):
    filtered_data: List[float] = Field(
        description="The filtered time series values after applying the Kalman filter"
    )
    raw_state: List[float] = Field(
        description="The raw state values from the Kalman filter"
    )
    smooth_state: List[float] = Field(
        description="The smoothed state values from the Kalman filter"
    )
    input_data: List[List[float]] = Field(
        description="The original input data"
    )
