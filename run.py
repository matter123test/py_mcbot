import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from config import load_config_from_file
from bot import Bot
import discord

CONFIG_FILE = "config.toml"

if __name__ == "__main__":
    config = load_config_from_file(CONFIG_FILE)
    intents = discord.Intents.default()
    bot = Bot(prefix="$", intents=intents, config=config)

    bot.run(config.bot.token)
