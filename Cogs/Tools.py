import asyncio
from dis import show_code
from re import search
import discord
from discord.commands import slash_command
from discord.ext import commands
from discord.ext import tasks

from hcspy import HCSClient
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
        await self.app.wait_until_ready()
        if str(time.localtime().tm_hour) == "6":
            with open("Data/selfcheck.dat", "rb") as selfcheck_data:
                selfcheck_list = pickle.load(selfcheck_data)
            for i in list(selfcheck_list.keys()):
                if str(selfcheck_list[str(i)]['error']) == "True":
                    continue
                result = await hcskr.asyncTokenSelfCheck(str(selfcheck_list[str(i)]['token']))
                dm_user = await self.app.fetch_user(int(i))
                embed = discord.Embed(title=f"Covid19 Auto Selfcheck Result", color=0x0AB1C2)
                embed.set_footer(text=f"Sented by Koi_Bot#4999ㆍAM 06:00 ~ AM 07:00 Auto COVID19 SelfCheck")
                embed.add_field(name = "Running Info", value = f"Code '{result['code']}' is returned.", inline = False)
                embed.add_field(name = "Code Info", value = f"{result['message']}", inline = False)
                embed.add_field(name = "Executed Time", value = f"Executed at {result['regtime']}.", inline = False)
                await dm_user.send(embed=embed)
            await Logger.info("Auto Covid19 Selfcheck executed.", self.app)    


 
    @slash_command(name = "selfcheck", guild_ids = [742201063972667487])
    async def selfcheck_command(self, ctx, name = None, birthday = None, school_name = None, password = None):
        if await Permission.check_permission(ctx, 1):
            return None
        with open("Data/selfcheck.dat", "rb") as selfcheck_data:
            selfcheck_list = pickle.load(selfcheck_data)
        if name == None:
            if str(ctx.author.id) not in selfcheck_list:
                embed = discord.Embed(title=f"자가진단 정보 등록법", color=0x0AB1C2)
                embed.set_footer(text=f"Sented by Koi_Bot#4999ㆍselfcheck Command's Result")
                embed.add_field(name = "How to register", value = "/selfcheck 이름 생년월일(YYMMDD) 학교이름 비밀번호(예제와 동일한 형식으로 입력해주세요.)", inline = False)
                embed.add_field(name = "Ex", value = "/selfcheck 홍길동 010101 서울중학교 1111", inline = False)
                embed.add_field(name = "Security", value = "모든 데이터는 평문의 형태로 저장되며, Koi_Bot#4999 및 KOI#4182가 이 데이터에 접근 할 수 있습니다.", inline = False)
                await ctx.respond(embed=embed)    
            else:
                result = await hcskr.asyncTokenSelfCheck(str(selfcheck_list[str(ctx.author.id)]['token']))
                embed = discord.Embed(title=f"Covid19 Auto Selfcheck Result", color=0x0AB1C2)
                embed.set_footer(text=f"Sented by Koi_Bot#4999ㆍselfcheck Command's Result")
                embed.add_field(name = "Running Info", value = f"Code '{result['code']}' is returned.", inline = False)
                embed.add_field(name = "Code Info", value = f"{result['message']}", inline = False)
                embed.add_field(name = "Executed Time", value = f"Executed at {result['regtime']}.", inline = False)
                await ctx.respond(embed=embed) 
        
        elif str(name) != "all":
            if birthday == None or school_name == None or password == None:
                await ctx.respond("무언가 빠졌어요! 다시 입력해주세요!", ephemeral = True)
            else:
                hcspy_client = HCSClient()
                hcspy_user_info = [str(name), str(birthday), str(school_name), str(password)]
                selfcheck_list[str(ctx.author.id)] = hcspy_user_info
                hcspy_user = await HCSClient.login_fast(name = name, school_name = school_name, birthday = birthday, password = password)
                print(await hcspy_user[-1].check())
                await ctx.respond(hcspy_user_info, ephemeral = True)
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
                embed.set_footer(text=f"Sented by Koi_Bot#4999ㆍAuto COVID19 SelfCheck Executed by {str(ctx.author)}")
                embed.add_field(name = "Running Info", value = f"Code '{result['code']}' is returned.", inline = False)
                embed.add_field(name = "Code Info", value = f"{result['message']}", inline = False)
                embed.add_field(name = "Executed Time", value = f"Executed at {result['regtime']}.", inline = False)
                embed.add_field(name = f"Executed by {str(ctx.author)}", value = "Maybe AutoSelfCheck would not be executed Automatically. (It was run manually.)", inline = False)
                await dm_user.send(embed=embed)

def setup(app):
    app.add_cog(Tools(app))