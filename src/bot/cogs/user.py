from discord.ext import commands
from discord import app_commands
import discord
import bot
import asyncio
from server.helpers import MCServerHelpers
import re


class User(commands.Cog):
    def __init__(self, bot: bot.Bot):
        self.bot = bot

    async def cog_load(self):
        print(f"{__name__} loaded!")

    @app_commands.command(name="start", description="Start the minecraft server")
    async def start(self, itn: discord.Interaction):
        if await MCServerHelpers.ensure_server_is_running(self.bot.server, itn):
            return

        self.bot.server.start()
        await itn.response.send_message("Starting the server!")

        while not self.bot.server.rcon.is_running():
            await asyncio.sleep(self.bot.config.mcrcon.delay_seconds)

        await itn.followup.send("Server is now online!")

    @app_commands.command(name="stop", description="Stop the minecraft server")
    async def stop(self, itn: discord.Interaction):
        if await MCServerHelpers.ensure_server_is_not_running(self.bot.server, itn):
            return

        if not await MCServerHelpers.ensure_server_is_empty(self.bot.server, itn):
            return

        await itn.response.send_message("Stopping the server!")

        self.bot.server.stop()

        while self.bot.server.rcon.is_running():
            await asyncio.sleep(self.bot.config.mcrcon.delay_seconds)

        await itn.followup.send("Server is now offline!")

    @app_commands.command(name="status", description="Get the minecraft server status")
    async def get_server_status(self, itn: discord.Interaction):
        if self.bot.server.is_running:
            await itn.response.send_message(f"Server is up and running!")
        else:
            await itn.response.send_message(f"Server is not running!")

    @app_commands.command(
        name="players", description="Get the online players in the minecraft server"
    )
    async def get_players(self, itn: discord.Interaction):
        if await MCServerHelpers.ensure_server_is_not_running(self.bot.server, itn):
            return

        output = self.bot.server.rcon.run_command("list")
        await itn.response.send_message(f"```{output}```")

    @app_commands.command(
        name="tps",
        description="Get the current ticks per second in the minecraft server",
    )
    async def get_tps(self, itn: discord.Interaction):
        if await MCServerHelpers.ensure_server_is_not_running(self.bot.server, itn):
            return

        output = self.bot.server.rcon.run_command("tps")

        if output:
            clean_msg = re.sub(r"§.", "", output)
            await itn.response.send_message(clean_msg)
        else:
            await itn.response.send_message("Operation failed")

    @app_commands.command(
        name="say", description="Sends a message to the minecraft server chat"
    )
    @app_commands.describe(message="The message you want to send")
    async def send_message(self, itn: discord.Interaction, message: str):
        if await MCServerHelpers.ensure_server_is_not_running(self.bot.server, itn):
            return

        author = itn.user.name
        self.bot.server.send_message(f"{author}: {message}")

        await itn.response.send_message("Message sent!")

    @app_commands.command(
        name="logs",
        description="Get the last 10 lines of the minecraft server logs file",
    )
    async def get_logs(self, itn: discord.Interaction):
        output = self.bot.server.get_logs()

        if output is not None:
            await itn.response.send_message(f"```{output}```")
        else:
            await itn.response.send_message("Logs are empty!")

    @app_commands.command(
        name="chat",
        description="Get the last 10 lines of player messages in the minecraft server chat",
    )
    async def chat(self, interaction: discord.Interaction):
        output = self.bot.server.get_player_messages()

        if output is not None:
            await interaction.response.send_message(f"```{output}```")
        else:
            await interaction.response.send_message("Chat is empty!")


async def setup(bot: bot.Bot):
    await bot.add_cog(User(bot))
