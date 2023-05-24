import discord
from discord.ext import commands
from discord.commands import slash_command

import subprocess

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
        embed = discord.Embed(title = '/test Koi_Bot Slash Result', description = 'Test Succeed. Result printed.', color = 0x00ffff)
        embed.add_field(name = "Embed's purpose", value = "To test Koi_Bot's Slash Command.", inline = False)
        await ctx.respond(embed = embed)

    @slash_command(name = "git_pull", guild_ids = SCS)
    async def git_pull_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        fd_popen = subprocess.Popen("git pull origin master", shell = True, stdout=subprocess.PIPE).stdout
        command_data = fd_popen.read().strip()
        fd_popen.close()
        embed = discord.Embed(title = '/test Koi_Bot Slash Result', description = 'git pull command', color = 0x00ffff)
        embed.add_field(name = "Result of the 'git pull origin master'", value = command_data, inline = False)
        await ctx.respond(embed = embed)
        await Logger.info("git pull command is activated", self.bot)

def setup(app):
    app.add_cog(Development(app))
