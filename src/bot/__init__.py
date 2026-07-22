from discord.ext import commands
from server import MCServer
import discord
import config


class Bot(commands.Bot):
    def __init__(
        self,
        prefix,
        intents: discord.Intents,
        config: config.Config,
    ):
        self.config = config
        self.server = MCServer(self.config)

        super().__init__(command_prefix=prefix, intents=intents)

    async def setup_hook(self):
        await self.load_extension("bot.cogs.user")
        await self.load_extension("bot.cogs.admin")

        self.tree.copy_global_to(guild=self.config.bot.guild)
        await self.tree.sync(guild=self.config.bot.guild)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_close(self):
        await super().close()
        print("Bot has been closed!")
