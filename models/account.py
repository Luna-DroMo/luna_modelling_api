from uuid import uuid4
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from models.base import Base
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "accounts"
    account_name = Column(String, unique=True, nullable=False, index=True)
    api_key = Column(UUID(as_uuid=True), unique=True,
                     nullable=False, default=uuid4, index=True)
    quota = Column(Integer, nullable=False, default=0)

    data = relationship("Data", back_populates="account")
