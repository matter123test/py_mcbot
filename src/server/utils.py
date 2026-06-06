import os.path
import re
from collections import deque

from mcrcon import MCRcon

from src import config


def run_mcrcon_command(command: str):
    with MCRcon(config.MCRCON_CONFIG.host, config.MCRCON_CONFIG.password, config.MCRCON_CONFIG.port) as mcr:
        resp = mcr.command(command)
        return resp


def get_tps() -> str:
    output = run_mcrcon_command("tps")
    return re.sub(r"§.", "", output)


def send_message(author: str, message: str):
    run_mcrcon_command(f"say {author}: {message}")


def get_logs(last_lines_count: int = 10) -> str | None:
    """
    Gets the last 10 lines of logs
    Note:
        The logs are read from the log file set in the server.config.json
    """
    if not os.path.exists(config.SERVER_CONFIG.server_logs_file_path):
        return None

    with open(config.SERVER_CONFIG.server_logs_file_path, "r", encoding="utf-8") as f:
        # older items are automatically dropped
        last_10_lines = deque(f, maxlen=last_lines_count)

    output = ''.join(last_10_lines)

    if len(output) > 0:
        return output
    else:
        return None


def get_player_messages(last_lines_count: int = 10) -> str | None:
    """
    Gets the last 10 messages sent by players in the minecraft server chat
    Note:
        The messages are read from the log file set in the server.config.json
    """

    with open(config.SERVER_CONFIG.server_logs_file_path, "r", encoding="utf-8") as f:
        # Get the last lines first
        last_lines = deque(f, maxlen=last_lines_count)

    lines = []

    for line in last_lines:
        # Example log: [10:54:30 INFO]: [Not Secure] <Jeb_theSheep_> 10
        # Regex str to separate the author and the message contents
        match = re.search(r"<([^>]+)>\s*(.*)", line)

        if match:
            author = match.group(1)
            content = match.group(2).strip()
            lines.append(f"{author}: {content}")

    output = '\n'.join(lines)

    if len(output) > 0:
        return output
    else:
        return None


def is_server_empty() -> bool:
    output = run_mcrcon_command("list")

    return "There are 0 of a max" in output
