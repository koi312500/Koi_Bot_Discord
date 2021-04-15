import discord
from discord.ext import commands
import hcskr
import pickle

from hcskr.hcs import asyncSelfCheck, selfcheck

from Config import Config
from Utils import Logger
from Utils.UserClass import UserClass as User
class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "selfcheck", help = "자가진단을 해 주는 명령어에요! 자세한 설명은 //selfcheck 를 통해 확인하세요!", usage = "//selfcheck 를 통해 확인하세요!")
    async def selfcheck_command(self, ctx, name = None, birth = None, region = None, school_name = None, school_type = None, password = None):
        
        with open("Data/selfcheck.dat", "rb") as selfcheck_data:
            selfcheck_list = pickle.load(selfcheck_data)
        if name == None:
            if str(ctx.author.id) not in selfcheck_list:
                await ctx.author.send("등록을 하기 위한 방법을 알려드릴게요!")
                await ctx.author.send("//selfcheck 이름 생년월일 지역 학교이름 학교종류 비밀번호")
                await ctx.author.send("Ex : //selfcheck 홍길동 010101 서울 서울중 중학교 1111")
                    
            else:
                await ctx.reply(await hcskr.asyncTokenSelfCheck(str(selfcheck_list[str(ctx.author.id)]['token']), customloginname = 'SelfCheck Executed by Koi_Bot#7938'), mention_author = False)
        
        else:
            if birth == None or region == None or school_name == None or school_type == None or password == None:
                await ctx.author.send("무언가 빠졌어요! 다시 입력해주세요!")
            else:
                token_hcskr = await hcskr.asyncGenerateToken(str(name), str(birth), str(region), str(school_name), str(school_type), str(password))
                selfcheck_list[str(ctx.author.id)] = token_hcskr
                await ctx.author.send(token_hcskr)
                with open("Data/selfcheck.dat", "wb") as selfcheck_data:
                    pickle.dump(selfcheck_list, selfcheck_data)

    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx, value_tmp):
        if ctx.author.id not in Config.admin_id:
            embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
            await ctx.reply(embed = embed, mention_author = False)
            return

        player = User(ctx.author)
        await ctx.reply(f"{str(ctx.author)} 님의 현재 잔고는 {player.money} 입니다.")
        with open("Data/selfcheck.dat", "wb+") as f: # 파일을 만들기
            selfcheck_list = dict()
            pickle.dump(selfcheck_list, f)

def setup(app):
    app.add_cog(Development(commands))