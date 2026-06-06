import discord
from discord.ext import commands

from src import config
from src.logger import Logger

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)


async def load_extensions():
    cogs = [
        "help",
        "admin_utils",
        "user_utils"
    ]

    for cog in cogs:
        await bot.load_extension(f"src.bot.cogs.{cog}")


async def main():
    Logger.log("Bot is now running!")

    async with bot:
        await load_extensions()
        await bot.start(config.BOT_CONFIG.token)


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)
