from mcrcon import MCRcon
import config


class MCServerRcon:
    def __init__(self, config: config.Config) -> None:
        self.config = config

    def run_command(self, cmd: str) -> str | None:
        with MCRcon(
            self.config.mcrcon.host,
            self.config.mcrcon.password,
            self.config.mcrcon.port,
        ) as rcon:
            response = rcon.command(cmd)
            return response

        return None

    def is_running(self) -> bool:
        try:
            self.run_command("list")
            return True
        except:
            return False
