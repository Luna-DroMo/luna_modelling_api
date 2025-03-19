from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from models.base import Base
from sqlalchemy.orm import relationship


class Data(Base):
    __tablename__ = "data"
    unique_identifier = Column(String, index=True)
    data = Column(JSONB, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    account = relationship("Account", back_populates="data")
