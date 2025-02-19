from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from models.account import Account
from core.deps import verify_api_key
from typing import List

router = APIRouter(prefix="/v1", tags=["kalman"])


class KalmanInput(BaseModel):
    data: List[float]


@router.post("/{account_id}/kalman")
async def kalman_filter(account_id, data: KalmanInput, currect_account: Account = Depends(verify_api_key)):
    if (currect_account != account_id):
        raise HTTPException(status_code=404, detail="Account not found.")

    try:

        # There will be modelling logic.
        return {"processed_results": data.results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
