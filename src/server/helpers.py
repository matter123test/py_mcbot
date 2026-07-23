import discord
import server


class MCServerHelpers:
    @staticmethod
    async def ensure_server_is_running(
        server: server.MCServer, itn: discord.Interaction
    ):
        if server.is_running:
            await itn.response.send_message("Server is already running!")
            return True

        return False

    @staticmethod
    async def ensure_server_is_not_running(
        server: server.MCServer, itn: discord.Interaction
    ):
        if not server.is_running:
            await itn.response.send_message("Server is not running!")
            return True

        return False

    @staticmethod
    async def ensure_server_is_empty(server: server.MCServer, itn: discord.Interaction):
        output = server.rcon.run_command("list")

        if output:
            if "There are 0 of a max" not in output:
                await itn.response.send_message("Server is not empty!")
                return False
            else:
                return True
        else:
            return True

    @staticmethod
    async def ensure_user_is_admin(server: server.MCServer, itn: discord.Interaction):
        if itn.user.id in server.config.bot.admins:
            return False
        else:
            await itn.response.send_message("Unauthorized access", ephemeral=True)
            return True
