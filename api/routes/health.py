from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    return {"status": "healthy"}


@router.get("/db")
async def db_health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Test database connection
        await db.execute("SELECT 1")
        return {"status": "database is healthy"}
    except Exception as e:
        return {"status": "database is unhealthy", "details": str(e)}
