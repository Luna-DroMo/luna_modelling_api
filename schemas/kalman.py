from pydantic import BaseModel, Field, model_validator
from typing import List, Optional


class KalmanInput(BaseModel):
    results: List[List[float]] = Field(
        description="A 2D array where each inner list contains time series values. "
                    "Example: [[10.2, 10.5, 10.1, 9.8, 10.3]]"
    )
    save: bool = Field(
        default=False,
        description="Whether to save the results to the database"
    )
    unique_identifier: Optional[str] = Field(
        default=None,
        description="The unique identifier for the data"
    )

    @model_validator(mode="after")
    def validate_unique_identifier_if_save(self) -> 'KalmanInput':
        """
        Validate that unique_identifier is provided when save is True.
        """
        if self.save and not self.unique_identifier:
            raise ValueError("unique_identifier is required when save is True")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "results": [[10.2, 10.5, 10.1, 9.8, 10.3]],
                "save": False,
                "unique_identifier": None
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
