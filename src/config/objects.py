from dataclasses import dataclass
import discord


@dataclass
class Bot:
    token: str
    guild: discord.Object
    admins: list[int]


@dataclass
class Server:
    folder: str
    log: str
    run: list[str]


@dataclass
class MCRcon:
    host: str
    password: str
    port: int
    delay_seconds: float


@dataclass
class Config:
    bot: Bot
    server: Server
    mcrcon: MCRcon
