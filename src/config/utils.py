import os

from src.config.globals import BOT_CONFIG_FILE_PATH, MCRCON_CONFIG_FILE_PATH, SERVER_CONFIG_FILE_PATH
from src.logger import Logger

files_to_check = [
    BOT_CONFIG_FILE_PATH,
    MCRCON_CONFIG_FILE_PATH,
    SERVER_CONFIG_FILE_PATH
]


def check_files():
    Logger.log("Checking for config files")

    for path in files_to_check:
        if not os.path.exists(path):
            Logger.err(f"file {path} does not exist")
            exit(1)

    Logger.log("Config files exist")