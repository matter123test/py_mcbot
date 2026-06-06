import discord
from discord.ext import commands

help_msg = """```
List of commands:
1) help         - Displays this list of commands
2) start        - Starts the minecraft server
3) stop         - Stops the minecraft server
4) status       - Gets the current minecraft server status
5) players      - Gets the player count in the minecraft server
6) tps          - Gets the current ticks per second in the minecraft server
7) say          - Sends a message to the minecraft server chat
8) logs         - Gets the last 10 lines of minecraft server logs
9) chat         - Gets the last 10 lines of minecraft server chat

Admin commands:
1) forcestop    - Stops the server even if there are players active in the server
2) exec         - Executes a command in the server. Example: $exec ban user
```"""


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: discord.ext.commands.Context):
        await ctx.send(help_msg)


async def setup(bot: discord.ext.commands.Bot):
    await bot.add_cog(Help(bot))
