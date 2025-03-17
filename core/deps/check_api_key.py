
from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import get_db
from models.account import Account
from uuid import UUID

api_key_header = APIKeyHeader(name="X-API-KEY")


async def verify_api_key(api_key: str = Security(api_key_header), db: AsyncSession = Depends(get_db)):
    try:
        api_key_uuid = UUID(api_key)
        query = select(Account).where(Account.api_key == api_key_uuid)
        result = await db.execute(query)
        account = result.scalar_one_or_none()

        if not account:
            raise HTTPException(status_code=403, detail="Invalid API key")
        return account

    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid API key format")
