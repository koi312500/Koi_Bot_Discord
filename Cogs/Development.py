import discord
from discord.ext import commands
import subprocess
import platform

class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.is_owner()
    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx, value_tmp):
        await ctx.reply("Hello, World!", mention_author = False)                                

def setup(app):
    app.add_cog(Development(commands))