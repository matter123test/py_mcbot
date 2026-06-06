from asyncio import sleep

import discord
from discord.ext import commands

from src import config
from src.server import server, run_mcrcon_command


class AdminUtils(commands.Cog):
    """This is a cog with admin-only commands
    Note:
        The admins are defined in bot.config.json
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="exec", description="Execute a command on the minecraft server")
    async def execute_command(self, ctx: discord.ext.commands.Context):
        if ctx.author.id not in config.BOT_CONFIG.admins:
            await ctx.send("Unauthorized access")
            return

        if not server.is_mcrcon_running():
            await ctx.send("Server is not running!")
            return

        cmd_to_run = ' '.join(ctx.message.content.split(' ')[1:])
        output = run_mcrcon_command(cmd_to_run)

        await ctx.send(output)

    @commands.command(name="forcestop", description="Stop the minecraft server even if there are players")
    async def force_stop(self, ctx: discord.ext.commands.Context):
        if ctx.author.id not in config.BOT_CONFIG.admins:
            await ctx.send("Unauthorized access")
            return

        if not server.is_mcrcon_running():
            await ctx.send("Server is not running!")
            return

        await ctx.reply("Stopping the server!")
        server.stop()

        while server.is_mcrcon_running():
            await sleep(config.MCRCON_CONFIG.secondsDelay)

        await ctx.reply("Server is now stopped!")


async def setup(bot: discord.ext.commands.Bot):
    await bot.add_cog(AdminUtils(bot))
