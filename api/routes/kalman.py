from fastapi import Depends, APIRouter, HTTPException
from models.account import Account
from core.deps.check_api_key import verify_api_key
from core.database import get_db
from core.deps.check_quota import check_quota
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.kalman import KalmanInput, KalmanOutput
from services.kalman import process_kalman_filter

router = APIRouter(tags=["kalman"])


@router.post("/{account_id}/kalman", response_model=KalmanOutput)
@check_quota
async def kalman_filter(
    account_id: int,
    kalman_input: KalmanInput,
    current_account: Account = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    if current_account.id != account_id:
        raise HTTPException(status_code=404, detail="Account not found.")

    try:

        input_data = kalman_input.results
        print("input_data: ", input_data)
        # Process the input data using the Kalman filter service
        filtered_data = process_kalman_filter(input_data)

        # Return the results
        return KalmanOutput(
            processed_results=filtered_data,
            input_data=input_data
        )

    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
