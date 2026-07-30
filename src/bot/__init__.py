from discord.ext import commands
from server import MCServer
from bot.utils import MCBotUtils, MCServerStatus
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
        self.utils = MCBotUtils(self)

        super().__init__(command_prefix=prefix, intents=intents)

    async def setup_hook(self):
        # Clear old registered commands just in case
        self.tree.clear_commands(guild=self.config.bot.guild)

        await self.load_extension("bot.cogs.user")
        await self.load_extension("bot.cogs.admin")

        self.tree.copy_global_to(guild=self.config.bot.guild)
        await self.tree.sync(guild=self.config.bot.guild)
        print(f"Registered {len(self.tree.get_commands())} commands!")

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        
        await self.utils.set_server_status(MCServerStatus.OFFLINE)

    async def on_close(self):
        await super().close()
        print("Bot has been closed!")
