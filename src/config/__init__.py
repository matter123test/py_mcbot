from config.objects import *
import tomllib


def load_config_from_file(filename: str) -> Config:
    with open(filename, "rb") as f:
        data = tomllib.load(f)

    bot = Bot(
        data["bot"]["token"],
        discord.Object(data["bot"]["guild"]),
        data["bot"]["admins"],
    )
    server = Server(
        data["server"]["folder"], data["server"]["log"], data["server"]["run"]
    )

    mcrcon = data["server"]["mcrcon"]
    mcrcon = MCRcon(
        mcrcon["host"],
        mcrcon["password"],
        mcrcon["port"],
        mcrcon["delay_seconds"],
    )

    return Config(bot, server, mcrcon)
