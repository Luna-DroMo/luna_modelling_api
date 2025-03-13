from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from models.account import Account
from core.deps import verify_api_key
from typing import List, Dict, Any
import numpy as np
from modelling.kalman_filter import KalmanFilter
from modelling.constants import F, H, Q, R, x0

router = APIRouter(tags=["kalman"])


class KalmanInput(BaseModel):
    results: List[float]


class KalmanOutput(BaseModel):
    processed_results: List[float]
    input_data: List[float]


@router.get("/", include_in_schema=True)
async def root_test():
    print("Root test endpoint reached!")
    return {"message": "Root endpoint working"}


@router.post("/test", include_in_schema=True)
async def test_endpoint():
    print("Test endpoint reached!")
    return {"message": "Hello World"}


@router.post("/{account_id}/kalman", response_model=KalmanOutput)
async def kalman_filter(
    account_id: int,
    kalman_input: KalmanInput,
    current_account: Account = Depends(verify_api_key)
):
    print("Account id", account_id)
    print("Current account", current_account.id)
    if current_account.id != account_id:
        raise HTTPException(status_code=404, detail="Account not found.")

    try:
        # Convert input data to numpy array
        observations = np.array(kalman_input.results)

        # Create and run Kalman filter with constants from constants.py
        kf = KalmanFilter(F=F, H=H, Q=Q, R=R, x0=x0)

        predictions_state, predictions_cov, predictions_obs = kf.forward(
            observations)

        # Convert numpy arrays to Python lists for JSON serialization
        filtered_data = [float(obs[0][0]) for obs in predictions_obs]

        return KalmanOutput(
            processed_results=filtered_data,
            input_data=kalman_input.results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
