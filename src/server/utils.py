import re
from collections import deque

from mcrcon import MCRcon

from src.config import MCRCON_CONFIG
from src.config import SERVER_CONFIG


def run_mcrcon_command(command: str):
    with MCRcon(MCRCON_CONFIG.host, MCRCON_CONFIG.password, MCRCON_CONFIG.port) as mcr:
        resp = mcr.command(command)
        return resp


def get_tps() -> str:
    output = run_mcrcon_command("tps")
    return re.sub(r"§.", "", output)


def send_message(author: str, message: str):
    run_mcrcon_command(f"say {author}: {message}")


def get_logs(last_lines_count: int = 10) -> str:
    with open(SERVER_CONFIG.server_logs_file_path, "r", encoding="utf-8") as f:
        # older items are automatically dropped
        last_10_lines = deque(f, maxlen=last_lines_count)

    output = "".join(last_10_lines)

    return output


def get_player_messages(last_lines_count: int = 10) -> str:
    with open(SERVER_CONFIG.server_logs_file_path, "r", encoding="utf-8") as f:
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

    return f"```{'\n'.join(lines)}```"


def is_server_empty() -> bool:
    output = run_mcrcon_command("list")

    return "There are 0 of a max" in output
