from sqlalchemy import Column, Integer, Boolean, DateTime, String

from tg_bot.db.base import Base


class UserHistory(Base):
    __tablename__ = "user_history"

    record_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    url = Column(String, nullable=False)
    success = Column(Boolean, nullable=False)

