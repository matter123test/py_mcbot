import re

from discord.ext import commands
import discord
import time

from src.config import BOT_CONFIG
from src.server.utils import is_server_empty
from src.server.utils import get_player_messages
from src.server.utils import get_logs
from src.server.utils import get_tps, send_message
from src.server import run_mcrcon_command
from src.logger import Logger
from src.config import MCRCON_CONFIG

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

from src.server import Server
from src.config import SERVER_CONFIG

server = Server(SERVER_CONFIG)


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)


@bot.command()
async def start(ctx: discord.ext.commands.Context):
    if server.is_running():
        await ctx.reply("Server is already running!")
    else:
        Logger.log("Starting the server!")
        await ctx.reply("Starting the server!")
        server.start()

        while not server.is_running():
            time.sleep(MCRCON_CONFIG.secondsDelay)

        Logger.log("Server is now running!")
        await ctx.reply("Server is now running!")


@bot.command()
async def stop(ctx: discord.ext.commands.Context):
    if server.is_running():
        if not is_server_empty():
            await ctx.reply("There are players in the server!")
            return

        await ctx.reply("Stopping the server!")
        server.stop()

        while server.is_running():
            time.sleep(MCRCON_CONFIG.secondsDelay)

        await ctx.reply("Server is now stopped!")
    else:
        await ctx.reply("Server is not running!")


@bot.command()
async def status(ctx: discord.ext.commands.Context):
    if server.is_running():
        await ctx.reply(f"Server is up and running!")
    else:
        await ctx.reply(f"Server is not running!")


@bot.command()
async def players(ctx: discord.ext.commands.Context):
    if not server.is_running():
        await ctx.send("Server is not running!")
    else:
        output = run_mcrcon_command("list")
        await ctx.send(f"```{output}```")


@bot.command()
async def tps(ctx: discord.ext.commands.Context):
    if not server.is_running():
        await ctx.send("Server is not running!")
    else:
        await ctx.send(get_tps())


@bot.command()
async def say(ctx: discord.ext.commands.Context):
    if not server.is_running():
        await ctx.send("Server is not running!")
    else:
        author = ctx.author.name
        message = ' '.join(ctx.message.content.split(" ")[1:])

        send_message(author, message)

        await ctx.reply("Message sent!")


@bot.command()
async def logs(ctx: discord.ext.commands.Context):
    output = get_logs()
    await ctx.send(output)


@bot.command()
async def chat(ctx: discord.ext.commands.Context):
    output = get_player_messages()
    await ctx.send(output)


@bot.command()
async def help(ctx: discord.ext.commands.Context):
    help_msg = """```
    List of commands:
    1) help     - displays this list of commands
    2) start    - start the server
    3) stop     - stop the server if its empty
    4) status   - get the server status
    5) players  - get the current player count
    6) tps      - get the current ticks per second
    7) say      - send a message to the server
    8) logs     - send last 10 lines of logs
    9) chat     - send last 10 lines of player messages
    
    Admin commands:
    1) forcestop    - stops the server even if there are players
    2) exec         - executes a command in the server example: !exec ban user
    
    ```"""

    await ctx.send(help_msg)


## Admin commands

@bot.command()
async def forcestop(ctx: discord.ext.commands.Context):
    if ctx.author.id not in BOT_CONFIG.admins:
        await ctx.send("Unauthorized access")
        return

    if not server.is_running():
        await ctx.send("Server is not running!")
        return

    await ctx.reply("Stopping the server!")
    server.stop()

    while server.is_running():
        time.sleep(MCRCON_CONFIG.secondsDelay)

    await ctx.reply("Server is now stopped!")


@bot.command()
async def exec(ctx: discord.ext.commands.Context):
    if ctx.author.id not in BOT_CONFIG.admins:
        await ctx.send("Unauthorized access")
        return

    if not server.is_running():
        await ctx.send("Server is not running!")
        return

    cmd_to_run = ' '.join(ctx.message.content.split(' ')[1:])
    output = run_mcrcon_command(cmd_to_run)

    await ctx.send(output)
