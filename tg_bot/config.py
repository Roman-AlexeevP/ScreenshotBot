import pathlib
from dataclasses import dataclass

import dotenv


@dataclass
class TgBot:
    token: str
    admin_id: str
    root_dir: pathlib.Path
    redis: str
    fsm_mod: str = "in_memory"


@dataclass
class Config:
    tg_bot: TgBot


def load_config():
    config = dotenv.dotenv_values()
    return Config(
        tg_bot=TgBot(
            token=config.get("TOKEN"),
            admin_id=config.get("ADMIN_ID"),
            root_dir=pathlib.Path(__file__).parent.parent,
            fsm_mod=config.get("FSM_MOD"),
            redis=config.get("REDIS")),
    )
