import json
from dataclasses import dataclass


@dataclass(frozen=True)
class ServerConfig:
    server_path: str
    server_logs_file_path: str
    run: list[str]


def get_server_config(path: str) -> ServerConfig:
    data = json.load(open(path, "r", encoding='utf-8'))

    server_path = data["server_path"]
    server_logs_file_path = data["server_logs_file_path"]
    run = data["run"]

    return ServerConfig(server_path, server_logs_file_path, run)
