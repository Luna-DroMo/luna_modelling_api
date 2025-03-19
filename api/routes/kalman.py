from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.account import Account
from core.deps.check_api_key import verify_api_key
from core.database import get_db
from core.deps.check_quota import check_quota
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.kalman import KalmanInput, KalmanOutput
from services.kalman import process_kalman_filter
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["kalman"])


@router.post("/{account_id}/kalman", response_model=KalmanOutput)
@check_quota
async def kalman_filter(
    account_id: int,
    kalman_input: KalmanInput,
    current_account: Account = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Apply Kalman filtering to time series data.

    The input must be a 2D array with one or more inner lists containing time series values:

    Example:
    ```json
    {
        "results": [[10.2, 10.5, 10.1, 9.8, 10.3]],
        "save": false
    }
    ```

    If save is true, a special message will be returned instead of processing the filter.
    """
    if current_account.id != account_id:
        raise HTTPException(status_code=404, detail="Account not found.")

    try:
        # Process the input data using the Kalman filter service
        if kalman_input.save:
            result = await process_kalman_filter(
                input_data=kalman_input.results,
                save=kalman_input.save,
                unique_identifier=kalman_input.unique_identifier,
                db=db,
                account_id=account_id
            )
        else:
            result = await process_kalman_filter(
                input_data=kalman_input.results,
                save=False
            )

        # Check if we got a special message response
        if "message" in result:
            return JSONResponse(content={"message": result["message"]})

        # Return the results
        return KalmanOutput(
            filtered_data=result["filtered_data"],
            raw_state=result["raw_state"],
            smooth_state=result["smooth_state"],
            input_data=kalman_input.results
        )

    except ValueError as e:
        # Handle validation errors
        #  logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected error
        raise HTTPException(status_code=500, detail=str(e))
