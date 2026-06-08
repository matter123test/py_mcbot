import discord
from discord.ext import commands

from src import config
from src.bot.utils import set_server_status, MinecraftServerStatus
from src.logger import Logger


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix="$", intents=intents, help_command=None)

    async def on_ready(self):
        print(f"Logged on as {self.user}")
        await set_server_status(self, MinecraftServerStatus.OFFLINE)

    async def setup_hook(self) -> None:
        cogs = [
            "help",
            "admin_utils",
            "user_utils"
        ]

        for cog in cogs:
            cog_name = f"src.bot.cogs.{cog}"

            Logger.log(f"Loading {cog_name}")
            await self.load_extension(cog_name)

    async def on_message(self, message):
        if message.author == self.user:
            return

        await self.process_commands(message)

    async def close(self) -> None:
        Logger.log("Bot has been closed!")

        await super().close()


def main():
    Logger.log("Bot is now running!")

    bot = Bot()
    bot.run(config.BOT_CONFIG.token)
