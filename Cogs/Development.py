import discord
from discord.ext import commands
from discord.commands import slash_command

from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User

class Development(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[742201063972667487], name = "test")
    async def test_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        print(type(ctx))
        embed = discord.Embed(title = '/test Koi_Bot Slash Result', description = 'Test Succeed. Result printed.', color = 0x00ffff)
        embed.add_field(name = "Embed's purpose", value = "To test Koi_Bot's Slash Command.", inline = False)
        await ctx.respond(embed = embed)

def setup(app):
    app.add_cog(Development(app))
