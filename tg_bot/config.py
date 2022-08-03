import dotenv
from dataclasses import dataclass

@dataclass
class TgBot:
    token: str
    admin_id: int

@dataclass
class Config:
    tg_bot: TgBot


def load_config():
    config = dotenv.dotenv_values()
    return Config(
        tg_bot=TgBot(
            token=config.get("TOKEN"),
            admin_id=config.get("ADMIN_ID"))
    )