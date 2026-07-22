from enum import Enum
import bot
import discord


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
