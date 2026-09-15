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

    # Optional info
    server_info = None
    try:
        server_info = Server.Info(
            data["server"]["info"]["name"],
            data["server"]["info"]["version"]
        )
    except Exception:
        pass

    # Optional, backups are enabled only if its enabled
    backups = None
    try:
        backups = Server.Backups(
            data["server"]["backup"]["max_backups"],
            data["server"]["backup"]["save_file"],
            data["server"]["backup"]["world_folder"],
            data["server"]["backup"]["backups_folder"],
            Server.Backups.ArchiveType(data["server"]["backup"]["archive_type"]),                        
        )
    except Exception:
        pass

    server = Server(
        data["server"]["folder"], data["server"]["log"], data["server"]["run"],
        server_info,
        backups
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

    if config.server.backups:
        if not os.path.exists(config.server.backups.world_folder):
            print(f"CONFIG: world folder {config.server.backups.world_folder} does not exist!")
            return None

        # Valid archive types
        if config.server.backups.archive_type in ["zip", "tar", "gztar", "bztar", "xztar", "zstdtar"]:
            return None

    return config
