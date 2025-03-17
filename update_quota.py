import asyncio
from sqlalchemy import update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.account import Account

# Database connection string from .env
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/luna_modelling"


async def update_quota(account_id: int, new_quota: int):
    # Create async engine and session
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Update quota
    async with async_session() as session:
        # Option 1: Using ORM
        query = update(Account).where(
            Account.id == account_id).values(quota=new_quota)
        await session.execute(query)
        await session.commit()
        print(f"Updated quota for account {account_id} to {new_quota}")


async def main():
    # Update account with ID 1 to have 100 quota
    await update_quota(1, 100)

    # You can add more accounts here
    # await update_quota(2, 50)

if __name__ == "__main__":
    asyncio.run(main())
