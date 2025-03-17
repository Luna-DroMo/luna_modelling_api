from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from functools import wraps
from models.account import Account
from core.database import get_db
from typing import Callable, Any


async def check_and_decrement_quota(account_id: int, db: AsyncSession) -> bool:
    """
    Check if quota is available and decrement atomically
    Returns True if quota was available and decremented, False otherwise
    """
    # Get current account with row lock to prevent race conditions
    query = select(Account).where(
        Account.id == account_id).with_for_update()
    result = await db.execute(query)
    account = result.scalar_one_or_none()

    if not account or account.quota <= 0:
        return False

    # Use raw SQL to update only the quota column without triggering updated_at
    # This avoids the timezone issue completely
    raw_sql = text(
        "UPDATE accounts SET quota = quota - 1 WHERE id = :account_id")
    await db.execute(raw_sql, {"account_id": account_id})

    # Commit the changes
    await db.commit()

    return True


def check_quota(func: Callable) -> Callable:
    """
    Decorator to check if an account has sufficient quota before 
    processing a request, and decrement quota if available
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract necessary parameters
        current_account = kwargs.get("current_account")
        db = kwargs.get("db")

        if not current_account or not db:
            # Try to get from dependencies if not in kwargs
            for arg in args:
                if isinstance(arg, Account):
                    current_account = arg
                elif isinstance(arg, AsyncSession):
                    db = arg

        if not current_account:
            raise HTTPException(
                status_code=500,
                detail="Implementation error: current_account not found"
            )

        if not db:
            # Get database session if not provided
            db = await get_db()

        # Check and decrement quota atomically
        quota_available = await check_and_decrement_quota(current_account.id, db)
        if not quota_available:
            raise HTTPException(
                status_code=403,
                detail="Quota exceeded. Please upgrade your plan."
            )

        # If quota was available and decremented, process the request
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            # If there's an error, we don't need to restore quota
            # since it was already decremented in the atomic operation
            raise e

    return wrapper
