from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from db.managers import UserHistoryManager


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, session_pool):
        super().__init__()
        self.session_pool = session_pool

    async def pre_process(self, obj, data, *args):
        async with self.session_pool() as session:
            data["session"] = session
            data["manager"] = UserHistoryManager(session=session)

    async def post_process(self, obj, data, *args):
        del data["manager"]
