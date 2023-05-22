import asyncio
import asyncio
import discord
import requests
from discord.commands import slash_command
from discord import option
from discord.ext import commands
from discord.ext import tasks

import pickle
import pytz
from datetime import datetime
import dateutil.tz as gettz

from config import Slash_Command_Server as SCS
import config
import Utils.login_utils as lu
from Utils import Logger
from Utils import Permission

timetable = [{''}]
class Tools(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.school_loop.start()
        self.school_study_loop.start()

    @tasks.loop(hours = 1)
    async def school_loop(self):
        await self.app.wait_until_ready()
        TIME_ZONE = pytz.timezone('Asia/Seoul')
        currentTime = datetime.now(TIME_ZONE)
        if int(currentTime.hour) == 6:
            with open("Data/SchoolInfo.dat", "rb") as school_data:
                school_member = pickle.load(school_data)
            for i in list(school_member.keys()):
                dm_user = await self.app.fetch_user(int(i))
                Food_type = ["아침", "점심", "저녁"]
                embed = discord.Embed(title=f"대전과학고 정보 알리미!", color=0x0AB1C2)
                embed.set_footer(text=f"Sented by Koi_Bot#4999ㆍAM 06:00 ~ AM 07:00 Auto School Info Command")
                url = config.meal_URL + str(currentTime.year) + str(currentTime.month).zfill(2) + str(currentTime.day).zfill(2) + config.meal_key
                data = requests.get(url).json()
                for j in range(0, 3):
                    now_check = str(data['mealServiceDietInfo'][1]['row'][j]['DDISH_NM'].replace('<br/>', '\n'))
                    embed.add_field(name = "급식 : " + str(Food_type[j]), value = now_check, inline = False)

                
                await dm_user.send(embed = embed)

    @tasks.loop(hours = 1)
    async def school_study_loop(self):
        LOGIN_URL = "https://djshs.kr/theme/s007/index/member_login.php"
        await self.app.wait_until_ready()
        TIME_ZONE = pytz.timezone('Asia/Seoul')
        currentTime = datetime.now(TIME_ZONE)
        if int(currentTime.hour) == 13:
            with open("Data/SchoolStudyInfo.dat", "rb") as school_data:
                school_member = pickle.load(school_data)
            print(school_member)
            for i in list(school_member.keys()):
                now_user = school_member[i]
                dm_user = await self.app.fetch_user(int(i))
                if now_user[0] == "Off":
                    continue
                embed = discord.Embed(title=f"대전과학고 자동 자습 신청 시스템!", color=0x0AB1C2)
                embed.set_footer(text=f"Sented by Koi_Bot#4999ㆍPM 01:00 ~ PM 02:00 Auto School Auto Study Command")
                try:
                    crawler = lu.LoginBot(LOGIN_URL)
                    crawler.login(now_user[1], now_user[2])
                    crawler.self_learning()
                    crawler.save_screenshot()
                    crawler.kill()
                    embed.add_field(name = "Info", value = f"자습 신청이 {now_user[3]}로 정상적으로 신청되었습니다!")
                    image = discord.File("test.png", filename="image.png")
                    await dm_user.send(embed = embed, file = image)
                except:
                    embed.add_field(name = "Info(Error)", value = f"자습 신청에 오류가 발생했습니다. 수동으로 신청하시기 바랍니다.")
                    await dm_user.send(embed = embed)

    @slash_command(name = "school_meal", guild_ids = SCS)
    async def school_meal_command(self, ctx, class_num : int):
        if await Permission.check_permission(ctx, 1):
            return None
        with open("Data/SchoolInfo.dat", "rb") as school_data:
            school_member = pickle.load(school_data)
        school_member[str(ctx.author.id)] = class_num
        with open("Data/SchoolInfo.dat", "wb") as school_data:
            pickle.dump(school_member, school_data)
        await ctx.respond(f"{str(ctx.author)}님이 학교 정보 알리미에 등록되었습니다!")
    
    @slash_command(name = "auto_study", guild_ids = SCS)
    @option("place", description="자습 신청하실 장소를 결정해 주세요.", choices=["교실(1-5)", "자습실"])
    @option("power", description="자동 자습 신청을 On/Off 하실지 결정해 주세요.", choices = ["On", "Off"])
    async def register_auto_study_command(self, ctx, power : str, place : str, id : str, password : str):
        if await Permission.check_permission(ctx, 1):
            return None
        message = await ctx.respond(f"입력하신 정보가 유효한 정보인지 확인하는 중입니다....", ephemeral = True)
        LOGIN_URL = "https://djshs.kr/theme/s007/index/member_login.php"
        try:
            crawler = lu.LoginBot(LOGIN_URL)
            crawler.login(id, password)
            crawler.kill()
        except:
            await message.edit_original_response(content = f"자습 신청에 오류가 발생한것으로 보여, 등록되지 않았습니다. (입력한 값의 오류, 또는 서버의 문제로 발생합니다.)")
            try:
                crawler.kill()
            except:
                pass
            return None

        with open("Data/SchoolStudyInfo.dat", "rb") as school_data:
            school_member = pickle.load(school_data)
        school_member[str(ctx.author.id)] = [power, id, password, place]
        with open("Data/SchoolStudyInfo.dat", "wb") as school_data:
            pickle.dump(school_member, school_data)
        await message.edit_original_response(content = f"{ctx.author}님의 자습 자동 신청 시스템이 {power} 되셨습니다.")


def setup(app):
    app.add_cog(Tools(app))