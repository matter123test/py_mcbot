from discord.ext import commands
from discord import app_commands
import discord
import bot
from server.helpers import MCServerHelpers
from bot.utils import MCBotUtils


class Admin(commands.Cog):
    def __init__(self, bot: bot.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"{__name__} loaded!")

    @app_commands.command(
        name="exec", description="Execute a command on the minecraft server"
    )
    @app_commands.describe(command="The command you want to run")
    async def execute_command(self, itn: discord.Interaction, command: str):
        if not await MCServerHelpers.ensure_user_is_admin(self.bot.server, itn):
            return

        if await MCServerHelpers.ensure_server_is_not_running(self.bot.server, itn):
            return

        output = self.bot.server.rcon.run_command(command)

        if output:
            await itn.response.send_message(f"```{output}```")
        else:
            await itn.response.send_message("Operation failed")

    @app_commands.command(
        name="forcestop",
        description="Stop the minecraft server even if there are players",
    )
    async def force_stop(self, itn: discord.Interaction):
        if not await MCServerHelpers.ensure_user_is_admin(self.bot.server, itn):
            return

        if await MCServerHelpers.ensure_server_is_not_running(self.bot.server, itn):
            return

        await MCBotUtils.stop_command(self.bot, itn)


async def setup(bot: bot.Bot):
    await bot.add_cog(Admin(bot))
