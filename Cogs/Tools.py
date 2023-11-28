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
from Utils import login_option as LO
from Utils import Logger
from Utils import Permission

timetable = [{''}]
class Tools(commands.Cog):
    def __init__(self, app):
        self.app = app
        self.school_loop.start()
        self.school_study_loop.start()

    class OptionView(discord.ui.View):
        @discord.ui.select(
            placeholder = "어디서 평일 자습을 하실 생각이신가요?",
            options = LO.discord_options,
            min_values = 1,
            max_values = 1
        )

        async def select_callback(self, select, interaction): # the function called when the user is done selecting options
            with open("Data/SchoolStudyInfo.dat", "rb") as school_data:
                school_member = pickle.load(school_data)
            school_member[str(interaction.user.id)][0] = "On"
            school_member[str(interaction.user.id)][3] = select.values[0]
            now_user = school_member[str(interaction.user.id)]
            with open("Data/SchoolStudyInfo.dat", "wb") as school_data:
                pickle.dump(school_member, school_data)
            message_content = f"{interaction.user}님의 자습 자동 신청 시스템이 {select.values[0]} 으로 On 되셨습니다."
            await interaction.response.send_message(content = message_content)
            TIME_ZONE = pytz.timezone('Asia/Seoul')
            currentTime = datetime.now(TIME_ZONE)
            if (int(currentTime.hour) >= 13 and int(currentTime.hour) < 18) or (int(currentTime.hour) == 18 and int(currentTime.minute) < 30):
                if int(currentTime.isoweekday()) >= 6:
                   return
                LOGIN_URL = "https://djshs.kr/theme/s007/index/member_login.php"
                embed = discord.Embed(title=f"대전과학고 자동 자습 신청 시스템!", color=0x0AB1C2)
                embed.set_footer(text=f"Sented by {config.bot_name}ㆍAuto School Auto Study Command")
                try:
                    crawler = lu.LoginBot(LOGIN_URL)
                except:
                    pass
                try:
                    crawler.login(now_user[1], now_user[2])
                    if now_user[1].startswith("2023") == False:
                        crawler.self_learning(now_user[3], 1)
                    else:
                        crawler.self_learning(now_user[3], 0)
                    crawler.save_screenshot()
                    crawler.kill()
                    embed.add_field(name = "Info", value = f"자습 신청이 {now_user[3]}로 정상적으로 신청되었습니다!")
                    image = discord.File("test.png", filename="image.png")
                    message_content = "장소 신청이 완료되었습니다. 이후에는 매일 1시 ~ 2시에 자동으로 진행됩니다. 1시 ~ 2시의 경우 자동 스케줄러와 충돌이 발생할 수 있습니다."
                    await interaction.followup.send(content = message_content, embed = embed, file = image)
                except:
                    try:
                        crawler.kill()
                    except:
                        pass
                    message_content = "장소 신청이 실패하였습니다. 미리 신청하셔둔 경우, 오류가 발생합니다. 1시 ~ 2시의 경우 자동 스케줄러와 충돌이 발생할 수 있습니다."
                    embed.add_field(name = "Info(Error)", value = f"자습 신청에 오류가 발생했습니다. 혹시 미리 신청하셨나요?")
                    await interaction.followup.send(content = message_content, embed = embed)



    @tasks.loop(hours = 1)
    async def school_loop(self):
        await self.app.wait_until_ready()
        TIME_ZONE = pytz.timezone('Asia/Seoul')
        currentTime = datetime.now(TIME_ZONE)
        if int(currentTime.hour) == 6:
            if int(currentTime.isoweekday()) >= 6:
                   return
            with open("Data/SchoolInfo.dat", "rb") as school_data:
                school_member = pickle.load(school_data)
            for i in list(school_member.keys()):
                try:
                    dm_user = await self.app.fetch_user(int(i))
                    Food_type = ["아침", "점심", "저녁"]
                    embed = discord.Embed(title=f"대전과학고 정보 알리미!", color=0x0AB1C2)
                    embed.set_footer(text=f"Sented by {config.bot_name}ㆍAM 06:00 ~ AM 07:00 Auto School Info Command")
                    url = config.meal_URL + str(currentTime.year) + str(currentTime.month).zfill(2) + str(currentTime.day).zfill(2) + config.meal_key
                    data = requests.get(url).json()
                    for j in range(0, 3):
                        try:
                            now_check = str(data['mealServiceDietInfo'][1]['row'][j]['DDISH_NM'].replace('<br/>', '\n'))
                            embed.add_field(name = "급식 : " + str(Food_type[j]), value = now_check, inline = False)
                        except:
                            pass

                    
                    await dm_user.send(embed = embed)
                except:
                    pass
            await Logger.info('School meal auto guide system activated.', self.app)

    async def school_study_func(self): # 등록된 모든 학생의 자습신청을 돌리는 함수
        LOGIN_URL = "https://djshs.kr/theme/s007/index/member_login.php"
        with open("Data/SchoolStudyInfo.dat", "rb") as school_data:
            school_member = pickle.load(school_data)
        for i in list(school_member.keys()):
            now_user = school_member[i]
            dm_user = None
            try:
                dm_user = await self.app.fetch_user(int(i))
            except:
                continue
            if now_user[0] == "Off":
                continue
            embed = discord.Embed(title=f"대전과학고 자동 자습 신청 시스템!", color=0x0AB1C2)
            embed.set_footer(text=f"Sented by {config.bot_name}ㆍPM 01:00 ~ PM 02:00 Auto School Auto Study Command")
            try:
                crawler = lu.LoginBot(LOGIN_URL)
            except:
                pass
            try:
                crawler.login(now_user[1], now_user[2])
                if now_user[1].startswith("2023") == False:
                    crawler.self_learning(now_user[3], 1)
                else:
                    crawler.self_learning(now_user[3], 0)
                crawler.save_screenshot()
                crawler.kill()
                embed.add_field(name = "Info", value = f"자습 신청이 {now_user[3]}로 정상적으로 신청되었습니다!")
                image = discord.File("test.png", filename="image.png")
                try:
                    await dm_user.send(embed = embed, file = image)
                except:
                    await Logger.info(f"Error, {dm_user}'s auto study application didn't work properly.\nAuto study application had activated, but DM is blocked.", self.app)
            except:
                try:
                    crawler.kill()
                except:
                    pass
                embed.add_field(name = "Info(Error)", value = f"자습 신청에 오류가 발생했습니다. 수동으로 신청하시기 바랍니다.")
                try:
                    await dm_user.send(embed = embed)
                except:
                    await Logger.info(f"Auto study application user {dm_user}'s DM is blocked. Cannot send message.", self.app)
                await Logger.info(f"Error, {dm_user}'s auto study application didn't work properly.", self.app)

    @tasks.loop(hours = 1)
    async def school_study_loop(self):
        await self.app.wait_until_ready()
        TIME_ZONE = pytz.timezone('Asia/Seoul')
        currentTime = datetime.now(TIME_ZONE)
        if int(currentTime.hour) == 13:
            if int(currentTime.isoweekday()) >= 6:
                   return
            All_Diet = True
            url = config.meal_URL + str(currentTime.year) + str(currentTime.month).zfill(2) + str(currentTime.day).zfill(2) + config.meal_key
            data = requests.get(url).json()
            for j in range(0, 3):
                try:
                    now_check = str(data['mealServiceDietInfo'][1]['row'][j]['DDISH_NM'].replace('<br/>', '\n'))
                except:
                    All_Diet = False
            if All_Diet == False:
                return
            await self.school_study_func()
            await Logger.info('School auto study appliction system activated.', self.app)

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
    @option("power", description="자동 자습 신청을 On/Off 하실지 결정해 주세요.", choices = ["On", "Off"])
    async def register_auto_study_command(self, ctx, power : str, id : str, password : str):
        if await Permission.check_permission(ctx, 1):
            return None
        
        if power == "Off":
            with open("Data/SchoolStudyInfo.dat", "rb") as school_data:
                school_member = pickle.load(school_data)
            school_member[str(ctx.author.id)] = ["Off", id, password, None]
            with open("Data/SchoolStudyInfo.dat", "wb") as school_data:
                pickle.dump(school_member, school_data)
            await ctx.respond(f"{ctx.author}님의 자동 자습 신청이 Off 되었습니다.")
            return None
        
        if id == "all" and password == "all":
            if await Permission.check_permission(ctx, 3):
                return None
    
            await ctx.respond("School auto study appliction system started manually.")
            await self.school_study_func()
            await Logger.info('School auto study appliction system activated manually.', self.app)
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
        school_member[str(ctx.author.id)] = ["Off", id, password, None]
        with open("Data/SchoolStudyInfo.dat", "wb") as school_data:
            pickle.dump(school_member, school_data)

        await message.edit_original_response(content = f"자습 신청 장소를 선택해 주세요.", view = self.OptionView(timeout = 20))


def setup(app):
    app.add_cog(Tools(app))
