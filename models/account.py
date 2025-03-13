from uuid import uuid4
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base


class Account(Base):
    __tablename__ = "accounts"
    account_name = Column(String, unique=True, nullable=False, index=True)
    api_key = Column(UUID(as_uuid=True), unique=True,
                     nullable=False, default=uuid4, index=True)
