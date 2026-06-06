import subprocess

from src import config
from src.config.parsers.server import ServerConfig
from src.server.utils import run_mcrcon_command
from src.logger import Logger


class Server:
    def __init__(self, server_config: ServerConfig):
        self.config = server_config

        self.process: subprocess.Popen | None = None
        self.is_server_running = False

    def start(self):
        if self.is_server_running:
            return

        self.is_server_running = True

        self.process = subprocess.Popen(
            self.config.run,
            cwd=self.config.server_path,
        )

    @staticmethod
    def is_mcrcon_running() -> bool:
        """
        This checks if the server is active via MCRcon
        Only works correctly if the server is already running
        """
        try:
            run_mcrcon_command("list")  # Dummy command to test if the server is running
            return True
        except Exception:
            Logger.warn("(mcrcon) Checking for sever status...")
            return False

    def stop(self):
        if not self.is_server_running:
            Logger.warn("Server is not running!!!")
            return

        if self.process is not None:
            try:
                run_mcrcon_command("stop")
            except Exception as e:
                Logger.err("Failed to stop the server", e)

            self.process.terminate()
            self.process.wait()

            self.is_server_running = False


server: Server = Server(config.SERVER_CONFIG)
