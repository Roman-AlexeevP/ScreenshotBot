from contextlib import suppress
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserHistory


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

        # some kind of compromiss for quick requestsfrom users
        with suppress(IntegrityError):
            await self.session.commit()
