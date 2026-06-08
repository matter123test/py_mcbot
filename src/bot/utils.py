from enum import Enum

import discord.ext


class MinecraftServerStatus(Enum):
    OFFLINE = 0
    ONLINE = 1
    STARTING = 2
    STOPPING = 3


def get_server_status_text(status: MinecraftServerStatus) -> str:
    if status is MinecraftServerStatus.OFFLINE:
        return "Server is offline!"
    elif status is MinecraftServerStatus.ONLINE:
        return "Server is online!"
    elif status is MinecraftServerStatus.STARTING:
        return "Server is starting!"
    elif status is MinecraftServerStatus.STOPPING:
        return "Server is stopping!"

    return "idk"


async def set_server_status(bot: discord.ext.commands.Bot, status: MinecraftServerStatus):
    status_text = get_server_status_text(status)

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.CustomActivity(
            name=status_text,
            type=discord.ActivityType.custom))
