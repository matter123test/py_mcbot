from src.config.utils import check_files
from src.config.globals import MCRCON_CONFIG_FILE_PATH
from src.config.parsers.mcrcon import get_mcrcon_config
from src.config.globals import BOT_CONFIG_FILE_PATH, SERVER_CONFIG_FILE_PATH
from src.config.parsers.bot import get_bot_config
from src.config.parsers.server import get_server_config

check_files()

BOT_CONFIG = get_bot_config(BOT_CONFIG_FILE_PATH)
SERVER_CONFIG = get_server_config(SERVER_CONFIG_FILE_PATH)
MCRCON_CONFIG = get_mcrcon_config(MCRCON_CONFIG_FILE_PATH)