import logging
from contextlib import suppress
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserHistory

logger = logging.getLogger(__file__)


class UserHistoryManager:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_action(self,
                         user_id: str,
                         url: str,
                         success: bool):
        """
        Save user action to db
        """
        entry = UserHistory()
        entry.user_id = user_id
        entry.url = url
        entry.success = success
        entry.created_at = datetime.utcnow()
        self.session.add(entry)

        logger.info(f"Action from user {user_id} saved to DB")

        # some kind of compromiss for quick requestsfrom users
        with suppress(IntegrityError):
            await self.session.commit()
