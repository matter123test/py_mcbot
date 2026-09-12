import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from config import load_config_with_validation
from bot import Bot
import discord
import subprocess

CONFIG_FILE = "config.toml"

if __name__ == "__main__":
    # Check if java exists
    try:
        output = subprocess.run(["java", "-version"])
    except FileNotFoundError:
        print("Java not found!")
        quit()

    config = load_config_with_validation(CONFIG_FILE)

    if config:
        print(config)

        intents = discord.Intents.default()
        bot = Bot(prefix="$", intents=intents, config=config)
        bot.run(config.bot.token)
    else:
        print(f"{CONFIG_FILE} is not valid!")
