import discord
from discord.ext import commands

class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.is_owner()
    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx, value_tmp):
        await ctx.channel.purge(limit = int(value_tmp))
        await ctx.send("숨 쉬는거 Freedom!")
    
    @commands.command(name = "Bot_Server")
    async def invite_server_command(self, ctx):
        await ctx.author.send("봇 서버 링크는 다음과 같습니다.")
        await ctx.author.send("https://discord.gg/qFZcgaN")

    @commands.command(name = "info")
    async def info_command(self,ctx):
        embed = discord.Embed(title=f"Koi_Bot Info", color=0x00ffff)
        embed.set_footer(text="현재 봇의 버전은 Beta 0.1 입니다.")
        embed.add_field(name = "Owner/Maker", value = "이 봇은 AKMU_LOVE#4211에 의해 제작되었습니다.", inline = False)
        embed.add_field(name = "License", value = "이 봇은 MIT License를 따르고 있습니다.", inline = False)
        embed.add_field(name = "Execution Environment", value = "현재, 이 봇은 LG 울트라북 15U560에서 동작중입니다.", inline = False)
        await ctx.channel.send(embed=embed)                                  

def setup(app):
    app.add_cog(Development(commands))