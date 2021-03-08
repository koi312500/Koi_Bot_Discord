import discord
from discord.ext import commands
import subprocess
import platform

from Config import Config
class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx, value_tmp):
        if ctx.author.id not in Config.admin_id:
            embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
            await ctx.reply(embed = embed, mention_author = False)
            return

        await ctx.reply("Hello, World!", mention_author = False)                                

def setup(app):
    app.add_cog(Development(commands))