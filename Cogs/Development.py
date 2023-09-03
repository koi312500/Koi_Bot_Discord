import discord
from discord.ext import commands
from discord.commands import slash_command

import subprocess

import config
from config import Slash_Command_Server as SCS
from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User

class Development(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name = "test", guild_ids = SCS)
    async def test_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        embed = discord.Embed(title = f'/test {config.bot_name} Slash Result', description = 'Test Succeed. Result printed.', color = 0x00ffff)
        embed.add_field(name = "Embed's purpose", value = f"To test {config.bot_name}'s Slash Command.", inline = False)
        await ctx.respond(embed = embed)

    @slash_command(name = "update", guild_ids = SCS)
    async def update_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        embed = discord.Embed(title = 'Update command Result', description = 'Remote update', color = 0x00ffff)
        fd_popen = subprocess.Popen("git pull origin master", shell = True, stdout=subprocess.PIPE).stdout
        command_data = fd_popen.read().strip()
        fd_popen.close()
        if len(command_data) > 1024:
            command_data = command_data[:700]
        embed.add_field(name = "Result of the `git pull origin master`", value = command_data, inline = False)
        print("Debug1 " + str(command_data))
        fd_popen = subprocess.Popen("pip install -r requirements.txt", shell = True, stdout=subprocess.PIPE).stdout
        command_data = fd_popen.read().strip()
        fd_popen.close()
        if len(command_data) > 1024:
            command_data = command_data[:700]
        embed.add_field(name = "Result of the `pip install -r requirements.txt`", value = command_data, inline = False)
        print("Debug2 " + str(command_data))
        embed.set_footer(text=f"Sented by {config.bot_name}ㆍUpdate Command")
        await ctx.respond(embed = embed)
        await Logger.info("update command is activated", self.bot)

def setup(app):
    app.add_cog(Development(app))
