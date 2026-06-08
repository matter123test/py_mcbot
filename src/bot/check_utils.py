import discord.ext
from discord.ext import commands

from src import config
from src.server import Server

import src.server.utils as server_utils


def is_user_id_admin():
    async def predicate(ctx: discord.ext.commands.Context):
        if not ctx.author.id in config.BOT_CONFIG.admins:
            await ctx.send("Unauthorized access")
            return False
        return True

    return commands.check(predicate)


def is_server_running(server: Server):
    async def predicate(ctx: discord.ext.commands.Context):
        if not server.is_mcrcon_running():
            await ctx.send("Server is not running!")
            return False
        return True

    return commands.check(predicate)


def is_server_not_running(server: Server):
    async def predicate(ctx: discord.ext.commands.Context):
        if server.is_mcrcon_running():
            await ctx.send("Server is already running!")
            return False
        return True

    return commands.check(predicate)


def is_server_empty():
    async def predicate(ctx: discord.ext.commands.Context):
        if not server_utils.is_server_empty():
            await ctx.reply("There are players in the server!")
            return False
        return True

    return commands.check(predicate)
