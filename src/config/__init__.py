from config.objects import *
import tomllib
import os


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


def load_config_with_validation(filename: str) -> Config | None:
    try:
        config = load_config_from_file(filename)
    except Exception as e:
        print(f"CONFIG INVALID: {e}")
        return None

    # Path validations
    if not os.path.exists(config.server.folder):
        print(f"CONFIG: server folder `{config.server.folder}` does not exist!")
        return None

    if not os.path.exists(config.server.log):
        print(f"CONFIG: logs file `{config.server.log}` does not exist!")
        return None

    return config
