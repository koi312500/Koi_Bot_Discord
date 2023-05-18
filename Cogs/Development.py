import discord
from discord.ext import commands
from discord.commands import slash_command

import os

from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User

class Development(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name = "test", guild_ids=[742201063972667487])
    async def test_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        embed = discord.Embed(title = '/test Koi_Bot Slash Result', description = 'Test Succeed. Result printed.', color = 0x00ffff)
        embed.add_field(name = "Embed's purpose", value = "To test Koi_Bot's Slash Command.", inline = False)
        await ctx.respond(embed = embed)

    @slash_command(name = "git_pull", guild_ids = [742201063972667487])
    async def git_pull_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        command_value = os.popen('git pull origin master').read()
        print("Test")
        embed = discord.Embed(title = '/test Koi_Bot Slash Result', description = 'git pull command', color = 0x00ffff)
        embed.add_field(name = "Result of the 'git pull origin master'", value = command_value, inline = False)
        await ctx.respond(embed = embed)

def setup(app):
    app.add_cog(Development(app))
