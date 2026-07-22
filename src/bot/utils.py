from enum import Enum
import bot
import discord
import asyncio


class MCServerStatus(Enum):
    OFFLINE = 0
    ONLINE = 1
    STARTING = 2
    STOPPING = 3

    @staticmethod
    def to_text(status: MCServerStatus) -> str:
        if status is MCServerStatus.OFFLINE:
            return "Server is offline!"
        elif status is MCServerStatus.ONLINE:
            return "Server is online!"
        elif status is MCServerStatus.STARTING:
            return "Server is starting!"
        elif status is MCServerStatus.STOPPING:
            return "Server is stopping!"

        return "idk"


class MCBotUtils:
    def __init__(self, bot: bot.Bot) -> None:
        self.bot = bot

    async def set_server_status(self, status: MCServerStatus):
        status_text = MCServerStatus.to_text(status)

        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.CustomActivity(
                name=status_text, type=discord.ActivityType.custom
            ),
        )

    @staticmethod
    async def start_command(bot: bot.Bot, itn: discord.Interaction):
        bot.server.start()
        await itn.response.send_message("Starting the server!")
        await bot.utils.set_server_status(MCServerStatus.STARTING)

        while not bot.server.rcon.is_running():
            await asyncio.sleep(bot.config.mcrcon.delay_seconds)

        await itn.followup.send("Server is now online!")
        await bot.utils.set_server_status(MCServerStatus.ONLINE)

    @staticmethod
    async def stop_command(bot: bot.Bot, itn: discord.Interaction):
        await itn.response.send_message("Stopping the server!")
        await bot.utils.set_server_status(MCServerStatus.STOPPING)

        bot.server.stop()

        while bot.server.rcon.is_running():
            await asyncio.sleep(bot.config.mcrcon.delay_seconds)

        await itn.followup.send("Server is now offline!")
        await bot.utils.set_server_status(MCServerStatus.OFFLINE)
