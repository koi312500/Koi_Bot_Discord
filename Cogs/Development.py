import discord
from discord.ext import commands

class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx):
        await ctx.channel.send(",안녕! 귀요미 마법사!")

    @commands.command(name = "Bot_Server")
    async def invite_server_command(self, ctx):
        await ctx.author.send("봇 서버 링크는 다음과 같습니다.")
        await ctx.author.send("https://discord.gg/qFZcgaN")



def setup(app):
    app.add_cog(Development(commands))