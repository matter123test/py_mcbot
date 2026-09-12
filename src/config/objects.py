from dataclasses import dataclass
import discord


@dataclass
class Bot:
    token: str
    guild: discord.Object
    admins: list[int]

    def __repr__(self) -> str:
        return f"---Bot---\n"\
               f"token:  ####################\n"\
               f"guild: {self.guild.id}\n"\
               f"admins: {self.admins}\n"\
               f"---Bot---\n"\


@dataclass
class Server:
    folder: str
    log: str
    run: list[str]
    info: Info | None

    @dataclass
    class Info:
        name: str
        version: str

        def __repr__(self) -> str:
            return f"---Server Info---\n"\
                   f"name: {self.name}\n"\
                   f"version: {self.version}\n"\
                   f"---Server Info---\n"

    def __repr__(self) -> str:
        return f"---Server---\n"\
               f"folder: {self.folder}\n"\
               f"log: {self.folder}\n"\
               f"run: {self.run}\n"\
               f"---Server---\n"

@dataclass
class MCRcon:
    host: str
    password: str
    port: int
    delay_seconds: float

    def __repr__(self) -> str:
        return f"---MCRcon---\n"\
               f"host: {self.host}\n"\
               f"password: ####################\n"\
               f"port: {self.port}\n"\
               f"delay_seconds: {self.delay_seconds}\n"\
               f"---MCRcon---\n"            


@dataclass
class Config:
    bot: Bot
    server: Server
    mcrcon: MCRcon

    def __repr__(self) -> str:
        return(
            f"{str(self.bot)}"\
            f"{str(self.server)}"\
            f"{str(self.server.info)}"\
            f"{str(self.mcrcon)}"
        )