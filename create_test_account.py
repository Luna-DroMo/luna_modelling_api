import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.account import Account
from core.config import settings


async def create_test_account():
    # Create async engine
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    # Create a test account
    async with async_session() as session:
        # Check if test account already exists
        from sqlalchemy import select
        query = select(Account).where(Account.name == "test_account")
        result = await session.execute(query)
        account = result.scalar_one_or_none()

        if account:
            print(f"Test account already exists with ID: {account.id}")
            print(f"API Key: {account.api_key}")
        else:
            # Create new test account
            test_account = Account(name="test_account")
            session.add(test_account)
            await session.commit()
            await session.refresh(test_account)

            print(f"Created test account with ID: {test_account.id}")
            print(f"API Key: {test_account.api_key}")

        # Return account ID and API key for testing
        return account.id if account else test_account.id, account.api_key if account else test_account.api_key

if __name__ == "__main__":
    account_id, api_key = asyncio.run(create_test_account())

    # Update the test script with the account ID and API key
    print("\nUpdate test_kalman.py with the following values:")
    print(f"account_id = \"{account_id}\"")
    print(f"api_key = \"{api_key}\"")
