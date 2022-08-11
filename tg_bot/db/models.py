from sqlalchemy import Column, Integer, BigInteger, Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from tg_bot.db.base import Base


class UserHistory(Base):
    __tablename__ = "userhistory"

    user_id = Column(UUID, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    url = Column(String, nullable=False)
    success = Column(Boolean, nullable=False)