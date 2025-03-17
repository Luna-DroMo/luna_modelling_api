from fastapi import Depends, APIRouter, HTTPException
from models.account import Account
from core.deps.check_api_key import verify_api_key
from core.database import get_db
from core.deps.check_quota import check_quota
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.panas import PanasInput, PanasOutput
from services.panas import process_panas_form

router = APIRouter(tags=["panas"])


@router.post("/{account_id}/panas", response_model=PanasOutput)
@check_quota
async def process_panas(
    account_id: int,
    panas_input: PanasInput,
    current_account: Account = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Process PANAS (Positive and Negative Affect Schedule) form data.

    Takes an array of 20 Likert scale responses (1-5) and returns
    Positive Affect (PA) and Negative Affect (NA) scores.

    This endpoint requires a valid API key and consumes one quota unit.
    """
    # Verify account access
    if current_account.id != account_id:
        raise HTTPException(status_code=404, detail="Account not found.")

    try:
        # Process the PANAS form data
        pa_na = process_panas_form(panas_input.results)

        # Return the results
        return PanasOutput(
            positive_affect=float(pa_na[0]),
            negative_affect=float(pa_na[1]),
            input_data=panas_input.results
        )

    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
