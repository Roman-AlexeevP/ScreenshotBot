import dotenv
from dataclasses import dataclass
import pathlib


@dataclass
class TgBot:
    token: str
    admin_id: str
    root_dir: pathlib.Path


@dataclass
class Config:
    tg_bot: TgBot


def load_config():
    config = dotenv.dotenv_values()
    return Config(
        tg_bot=TgBot(
            token=config.get("TOKEN"),
            admin_id=config.get("ADMIN_ID"),
            root_dir=pathlib.Path(__file__).parent.parent)
    )
