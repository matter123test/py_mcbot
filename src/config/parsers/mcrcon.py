from dataclasses import dataclass
import json


@dataclass(frozen=True)
class MCRconConfig:
    host: str
    password: str
    port: int
    secondsDelay: float


def get_mcrcon_config(path: str) -> MCRconConfig:
    data = json.load(open(path, "r", encoding='utf-8'))

    host = data["host"]
    password = data["password"]
    port = data["port"]
    seconds_delay = data["seconds_delay"]

    return MCRconConfig(host, password, port, seconds_delay)
