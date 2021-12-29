import asyncio
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ext import tasks

import hcskr
import pickle
import time

from Utils import Logger
from Utils import Permission

class Tools(commands.Cog):

    def __init__(self, app):
        self.app = app
        self.selfcheck_loop.start()

    @tasks.loop(hours = 1)
    async def selfcheck_loop(self):
        print(time.localtime().tm_hour)
        if str(time.localtime().tm_hour) == "6":
            with open("Data/selfcheck.dat", "rb") as selfcheck_data:
                selfcheck_list = pickle.load(selfcheck_data)
            for i in list(selfcheck_list.keys()):
                if str(selfcheck_list[str(i)]['error']) == "True":
                    continue
                result = await hcskr.asyncTokenSelfCheck(str(selfcheck_list[str(i)]['token']))
                dm_user = await self.app.fetch_user(int(i))
                embed = discord.Embed(title=f"Covid19 Auto Selfcheck Result", color=0x0AB1C2)
                embed.set_footer(text=f"AM 06:00 ~ AM 07:00 Auto COVID19 SelfCheck")
                embed.add_field(name = "Running Info", value = f"Code '{result['code']}' is returned.", inline = False)
                embed.add_field(name = "Code Info", value = f"{result['message']}", inline = False)
                embed.add_field(name = "Executed Time", value = f"Executed at {result['regtime']}.", inline = False)
                await dm_user.send(embed=embed)
            await Logger.info("Auto Covid19 Selfcheck executed.", self.app)    


 
    @slash_command(name = "selfcheck", help = "자가진단을 해 주는 명령어에요! 자세한 설명은 //selfcheck 를 통해 확인하세요!", usage = "//selfcheck 를 통해 확인하세요!", guild_ids = [742201063972667487])
    async def selfcheck_command(self, ctx, name = None, birth = None, region = None, school_name = None, school_type = None, password = None):
        if await Permission.check_permission(ctx, 1):
            return None
        with open("Data/selfcheck.dat", "rb") as selfcheck_data:
            selfcheck_list = pickle.load(selfcheck_data)
        if name == None:
            if str(ctx.author.id) not in selfcheck_list:
                embed = discord.Embed(title=f"자가진단 정보 등록법", color=0x0AB1C2)
                embed.set_footer(text=f"'hcskr' python 모듈을 사용중입니다.")
                embed.add_field(name = "How to register", value = "//selfcheck 이름 생년월일(YYMMDD) 지역 학교이름 학교유형 비밀번호", inline = False)
                embed.add_field(name = "Ex", value = "//selfcheck 홍길동 010101 서울 서울중 중학교 1111", inline = False)
                embed.add_field(name = "Security", value = "사용자의 개인정보 보호를 위해, hcskr 모듈의 token 자가진단 함수를 사용중입니다.\nKoi_Bot 에서는, //selfcheck로 시작되는 모든 기록을 로깅하지 않습니다.", inline = False)
                await ctx.respond(embed=embed)    
            else:
                result = await hcskr.asyncTokenSelfCheck(str(selfcheck_list[str(ctx.author.id)]['token']))
                embed = discord.Embed(title=f"Covid19 Auto Selfcheck Result", color=0x0AB1C2)
                embed.set_footer(text=f"//selfcheck 명령어의 결과입니다.")
                embed.add_field(name = "Running Info", value = f"Code '{result['code']}' is returned.", inline = False)
                embed.add_field(name = "Code Info", value = f"{result['message']}", inline = False)
                embed.add_field(name = "Executed Time", value = f"Executed at {result['regtime']}.", inline = False)
                await ctx.respond(embed=embed) 
        
        elif str(name) != "all":
            if birth == None or region == None or school_name == None or school_type == None or password == None:
                await ctx.respond("무언가 빠졌어요! 다시 입력해주세요!", ephemeral = True)
            else:
                token_hcskr = await hcskr.asyncGenerateToken(str(name), str(birth), str(region), str(school_name), str(school_type), str(password))
                selfcheck_list[str(ctx.author.id)] = token_hcskr
                await ctx.respond(token_hcskr, ephemeral = True)
                with open("Data/selfcheck.dat", "wb") as selfcheck_data:
                    pickle.dump(selfcheck_list, selfcheck_data)
        
        else:
            await Logger.info(f"Covid19 Selfcheck executed by {str(ctx.author)}. (It was run manually.)", self.app)
            with open("Data/selfcheck.dat", "rb") as selfcheck_data:
                selfcheck_list = pickle.load(selfcheck_data)
            for i in list(selfcheck_list.keys()):
                if str(selfcheck_list[str(i)]['error']) == "True":
                    continue
                result = await hcskr.asyncTokenSelfCheck(str(selfcheck_list[str(i)]['token']))
                dm_user = await self.app.fetch_user(int(i))
                embed = discord.Embed(title=f"Covid19 Auto Selfcheck Result", color=0x0AB1C2)
                embed.set_footer(text=f"Auto COVID19 SelfCheck Executed by {str(ctx.author)}")
                embed.add_field(name = "Running Info", value = f"Code '{result['code']}' is returned.", inline = False)
                embed.add_field(name = "Code Info", value = f"{result['message']}", inline = False)
                embed.add_field(name = "Executed Time", value = f"Executed at {result['regtime']}.", inline = False)
                embed.add_field(name = f"Executed by {str(ctx.author)}", value = "Maybe AutoSelfCheck would not be executed Automatically. (It was run manually.)", inline = False)
                await dm_user.send(embed=embed)

def setup(app):
    app.add_cog(Tools(app))