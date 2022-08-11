from typing import Callable, Awaitable, Dict, Any

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types.base import TelegramObject

from db.managers import UserHistoryManager


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            data["manager"] = UserHistoryManager(session=session)
            return await handler(event, data)
