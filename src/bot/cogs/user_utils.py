from asyncio import sleep

import discord
from discord.ext import commands

from src import config
from src.logger import Logger
from src.server import server
from src.server.utils import is_server_empty, run_mcrcon_command, get_tps, send_message, get_logs, get_player_messages


class UserUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="start", description="Start the minecraft server")
    async def start_server(self, ctx: discord.ext.commands.Context):
        if server.is_server_running:
            Logger.warn("Ignoring $start request")
            await ctx.reply("Server is already running!")
            return

        Logger.log("Starting the server!")
        await ctx.reply("Starting the server!")
        server.start()

        while not server.is_mcrcon_running():
            await sleep(config.MCRCON_CONFIG.secondsDelay)

        Logger.log("Server is now running!")
        await ctx.reply("Server is now running!")

    @commands.command(name="stop", description="Stop the minecraft server")
    async def stop_server(self, ctx: discord.ext.commands.Context):
        if not server.is_server_running:
            Logger.warn("Ignoring $stop request")
            await ctx.reply("Server is not running!")

        if not is_server_empty():
            await ctx.reply("There are players in the server!")
            return

        await ctx.reply("Stopping the server!")
        server.stop()

        while server.is_mcrcon_running():
            await sleep(config.MCRCON_CONFIG.secondsDelay)

        await ctx.reply("Server is now stopped!")

    @commands.command(name="status", description="Get the minecraft server status")
    async def get_server_status(self, ctx: discord.ext.commands.Context):
        if server.is_mcrcon_running():
            await ctx.reply(f"Server is up and running!")
        else:
            await ctx.reply(f"Server is not running!")

    @commands.command(name="players", description="Get the online players in the minecraft server")
    async def get_players(self, ctx: discord.ext.commands.Context):
        if not server.is_mcrcon_running():
            await ctx.send("Server is not running!")
        else:
            output = run_mcrcon_command("list")
            await ctx.send(f"```{output}```")

    @commands.command(name="tps", description="Get the current ticks per second in the minecraft server")
    async def get_tps(self, ctx: discord.ext.commands.Context):
        if not server.is_mcrcon_running():
            await ctx.send("Server is not running!")
        else:
            await ctx.send(get_tps())

    @commands.command(name="say", description="Sends a message to the minecraft server chat")
    async def send_message(self, ctx: discord.ext.commands.Context):
        if not server.is_mcrcon_running():
            await ctx.send("Server is not running!")
        else:
            author = ctx.author.name
            message = ' '.join(ctx.message.content.split(" ")[1:])

            send_message(author, message)

            await ctx.reply("Message sent!")

    @commands.command(name="logs", description="Get the first 10 lines of the minecraft server logs")
    async def get_logs(self, ctx: discord.ext.commands.Context):
        output = get_logs()
        await ctx.send(output)

    @commands.command(name="chat", description="Get the first 10 lines of player messages in the minecraft server chat")
    async def chat(self, ctx: discord.ext.commands.Context):
        output = get_player_messages()
        await ctx.send(output)


async def setup(bot: discord.ext.commands.Bot):
    await bot.add_cog(UserUtils(bot))
