import discord
from discord.ext import commands

from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User
class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx, value_tmp):
        if await Permission.check_permission(ctx, 3):
            return None
        await ctx.reply("Hello, World!")

    @commands.command(name = "me")
    async def myinfo_show_command(self, ctx):
        permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
        now_user = User(ctx.author)
        embed = discord.Embed(title=f"{str(now_user.name)} 님의 Koi_Bot Info", color=0x00ffff)
        embed.set_footer(text="//me 명령어의 결과입니다.")
        embed.add_field(name = "현재 레벨", value = f"{now_user.level}레벨, {now_user.exp} exp를 가지고 있어요! ", inline = False)
        embed.add_field(name = "Permission", value = f"현재 권한 등급 : {str(permission_message[int(now_user.permission)])}")
        await ctx.reply(embed=embed)  

def setup(app):
    app.add_cog(Development(app))