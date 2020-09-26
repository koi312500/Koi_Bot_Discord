import discord
from discord.ext import commands

class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "test", help = "관리자용 커맨드입니다.")
    async def test_command(self, ctx):
        await ctx.channel.send("Test succeed!")

def setup(app):
    app.add_cog(Development(commands))