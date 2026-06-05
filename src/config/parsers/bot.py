from dataclasses import dataclass
import json


@dataclass(frozen=True)
class BotConfig:
    token: str
    admins: list[int]


def get_bot_config(path: str) -> BotConfig:
    data = json.load(open(path, "r", encoding="utf-8"))

    token = data["token"]
    admins = data["admins"]

    return BotConfig(token, admins)
