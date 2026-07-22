import subprocess
from config import Config
from server.rcon import MCServerRcon
import os
from collections import deque
import re


class MCServer:
    def __init__(self, config: Config) -> None:
        self.rcon = MCServerRcon(config)
        self.config = config

        self.is_running = False
        self.process: subprocess.Popen

    def start(self) -> None:
        if self.is_running:
            return

        self.process = subprocess.Popen(
            self.config.server.run,
            cwd=self.config.server.folder,
        )

        self.is_running = True

    def stop(self) -> None:
        print("Trying to stop")

        if not self.is_running:
            return

        print("Stopping!")

        try:
            self.rcon.run_command("stop")
        except Exception as e:
            print("FAILED", e)

        self.process.wait()

        print("Stopped the process")

        self.is_running = False

    def get_status(self) -> bool:
        return self.is_running

    def send_message(self, msg: str):
        self.rcon.run_command(f"say {msg}")

    def get_logs(self) -> str | None:
        """
        Gets the last 10 lines of logs
        Note:
            The logs are read from the log file set in the server.config.json
        """
        if not os.path.exists(self.config.server.log):
            return None

        with open(self.config.server.log, "r", encoding="utf-8") as f:
            # older items are automatically dropped
            last_10_lines = deque(f, maxlen=10)

        output = "".join(last_10_lines)

        if len(output) > 0:
            return output
        else:
            return None

    def get_player_messages(self) -> str | None:
        """
        Gets the last 10 messages sent by players in the minecraft server chat
        Note:
            The messages are read from the log file set in the server.config.json
        """

        with open(self.config.server.log, "r", encoding="utf-8") as f:
            # Get the last lines first
            last_lines = deque(f, maxlen=10)

        lines = []

        for line in last_lines:
            # Example log: [10:54:30 INFO]: [Not Secure] <Jeb_theSheep_> 10
            # Regex str to separate the author and the message contents
            match = re.search(r"<([^>]+)>\s*(.*)", line)

            if match:
                author = match.group(1)
                content = match.group(2).strip()
                lines.append(f"{author}: {content}")

        output = "\n".join(lines)

        if len(output) > 0:
            return output
        else:
            return None
