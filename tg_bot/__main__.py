import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.base import Base
from tg_bot.config import load_config
from tg_bot.handlers import users as users_handler
from tg_bot.middlewares import db

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config()

    # Creating DB engine for PostgreSQL
    psql_dsn = f"postgresql+asyncpg://{config.postgres.db_user}:{config.postgres.db_pass}" \
               f"@{config.postgres.db_host}/{config.postgres.db_name}"
    engine = create_async_engine(psql_dsn, echo=True)

    # Creating DB connections pool
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Storage init
    if config.tg_bot.fsm_mod == "redis":
        storage = RedisStorage.from_url(
            url=config.tg_bot.redis,
            connection_kwargs={"decode_responses": True}
        )
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    bot["root_dir"] = config.tg_bot.root_dir
    dp = Dispatcher(bot, storage=storage)

    dp.middleware.setup(db.DbMiddleware(db_pool))

    users_handler.register_user(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    cli()
