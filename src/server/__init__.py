import subprocess

from mcrcon import MCRconException

from src.config.parsers.server import ServerConfig
from src.server.utils import run_mcrcon_command
from src.logger import Logger


class Server:
    def __init__(self, config: ServerConfig):
        self.config = config

        self.process: subprocess.Popen | None = None

    def start(self):
        self.process = subprocess.Popen(
            self.config.run,
            cwd=self.config.server_path,
        )

    @staticmethod
    def is_running() -> bool:
        try:
            run_mcrcon_command("list")  # Dummy command to test if the server is running
            return True
        except Exception:
            Logger.warn("(mcrcon) Checking for sever status...")
            return False

    def stop(self):
        if self.process:

            try:
                run_mcrcon_command("stop")
            except Exception as e:
                Logger.err("Failed to stop the server", e)

            self.process.terminate()
            self.process.wait()
