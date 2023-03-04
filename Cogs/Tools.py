import asyncio
import discord
import requests
from discord.commands import slash_command
from discord.ext import commands
from discord.ext import tasks

import pickle
import pytz
from datetime import datetime
import dateutil.tz as gettz

import config
from Utils import Logger
from Utils import Permission

class Tools(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.school_loop.start()

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

    @slash_command(name = "register_school", guild_ids = [742201063972667487])
    async def register_school_command(self, ctx, class_num : int):
        if await Permission.check_permission(ctx, 1):
            return None
        with open("Data/SchoolInfo.dat", "rb") as school_data:
            school_member = pickle.load(school_data)
        school_member[str(ctx.author.id)] = class_num
        with open("Data/SchoolInfo.dat", "wb") as school_data:
            pickle.dump(school_member, school_data)
        await ctx.respond(f"{str(ctx.author)}님이 학교 정보 알리미에 등록되었습니다!")
        

def setup(app):
    app.add_cog(Tools(app))