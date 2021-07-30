import discord
from discord.ext import commands
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User

class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        embed = discord.Embed(title = ':fireworks: Welcome to "Hello, Discord" Server! :fireworks:', description = '저희 "Hello, Discord!" 서버에 오신 여러분을 환영합니다!', color = 0x00ffff)
        embed.add_field(name = "Server's purpose", value = "KOI#4182 가 만든 이상한 서버입니다! 심심한 사람들을 위한 대화 서버입니다!", inline = False)
        embed.add_field(name = "What you can do in this server", value = "다양한 사람들과 함꼐 여러가지 주제와 내용을 가지고 대화하세요! (코딩 관련 내용이 상대적으로 많지만, 그 외의 다양한 이야기도 가능하십니다!)", inline = False)
        embed.add_field(name = "Membership Screening", value = '저희 서버는 Membership Screening을 사용하여 서버 규칙에 대한 동의를 받고 있습니다! 동의를 해주시면 바로 서버에서 활동 하실 수 있습니다!', inline = False)
        embed.add_field(name = "Problem & QnA", value = f'궁금하신 점이 있으시면 서버 관리자인 {ctx.author.mention} 에게 물어봐 주세요!', inline = False)
        embed.set_footer(text = 'Written at 07.29ㆍSented by KOI#4182')
        await ctx.send(embed = embed)
def setup(app):
    app.add_cog(Development(app))