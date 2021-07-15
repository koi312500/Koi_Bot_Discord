import discord
import asyncio
from discord.ext import commands
from discord.ext import tasks

import time
import subprocess
import platform

from Utils import Permission
from Utils import Logger

class BotManagement(commands.Cog):

    def __init__(self, app):
        self.app = app
        self.status_change.start()

    @tasks.loop(seconds = 30)
    async def status_change(self):
        status_list = ["'//help' to check commands list!", "Made by KOI#4182(AKMU_LOVE#4211)"]
        for i in range(0,2):
            await asyncio.sleep(10)
            await self.app.change_presence(status = discord.Status.online, activity = discord.Game(status_list[i]))
    
    @commands.command(name = "update_delay", help = "봇 개발을 위하여 일시적으로 서버를 1시간 중지하는 명령어입니다.", usage = "//update_delay")
    async def update_delay_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        await Logger.info("1H Server stop for update is requested.", self.app)
        if str(platform.system()) == "Windows":
            await ctx.reply("Execution platform is **Windows**. Update_delay system for **Windows** is deleted by owner. No action.")
            await Logger.info("No action because execution platform is Windows.", self.app)
        elif str(platform.system()) == "Linux":
            await ctx.reply("Execution platform is **Linux**, Request to start update_delay.sh.")
            subprocess.call("./update_delay.sh &", shell = True)
            await Logger.info("Shell command './update_delay.sh &' is requested.", self.app)
            await Logger.info("Exiting progress.", self.app)
            await asyncio.sleep(3)
            await ctx.reply("Done. Exiting progress.")
            exit()
        else:
            Logger.info("Cannot detect execution platform. Cannot update automatically.",self.app)
            await ctx.reply("Cannot detect your execution platform. Cannot reboot your bot automatically.", self.app)
        

    @commands.command(name = "restart", help = "봇을 재부팅합니다.", usage = "//restart")
    async def restart_command(self,ctx):
        if await Permission.check_permission(ctx, 3):
            return None
          
        await Logger.info("Restarting is requested.", self.app)
        if str(platform.system()) == "Windows":
            await ctx.reply("Execution platform is **Windows**. Reboot system for **Windows** is deleted by owner. No action.")
            await Logger.info("No action because execution platform is Windows.", self.app)
        elif str(platform.system()) == "Linux":
            await ctx.reply("Execution platform is **Linux**, Request to start restart.sh.")
            subprocess.call("./restart.sh &", shell = True)
            await Logger.info("Shell command './restart.sh &' is requested.", self.app)
            await Logger.info("Exiting progress.", self.app)
            await asyncio.sleep(3)
            await ctx.reply("Done. Exiting progress.")
            exit()
        else:
            Logger.info("Cannot detect execution platform. Cannot update automatically.",self.app)
            await ctx.reply("Cannot detect your execution platform. Cannot reboot your bot automatically.", self.app)

    @commands.command(name = "stop", help = "봇을 종료합니다.", usage = "//stop")
    async def stop_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
          
        await Logger.info("Exiting progress.", self.app)
        await ctx.reply("Exiting progress.")
        exit()
   
    @commands.command(name = "invite", help = "Koi_Bot의 공식 서버 초대 링크를 보내드립니다.", usage = "//invite")
    async def invite_server_command(self, ctx):
        if await Permission.check_permission(ctx, 1):
            return None

        await ctx.author.send("봇 서버 링크는 다음과 같습니다.")
        await ctx.author.send("https://discord.gg/sX2K7eGdzT")
        await ctx.reply("Koi_Bot의 공식 서버 초대 링크가 DM으로 전송되었습니다!", mention_author = False)

    @commands.command(name = "info", help = "Koi_Bot의 정보를 출력합니다.", usage = "//info")
    async def info_command(self,ctx):
        if await Permission.check_permission(ctx, 1):
            return None
          
        embed = discord.Embed(title=f"Koi_Bot Info", color=0x00ffff)
        embed.set_footer(text=f"현재 봇의 버전은 Alpha 1.2.0 입니다.")
        embed.add_field(name = "Owner/Maker", value = "이 봇은 AKMU_LOVE#4211에 의해 제작되었습니다.", inline = False)
        embed.add_field(name = "License", value = "이 봇은 MIT License를 따르고 있습니다.", inline = False)
        embed.add_field(name = "Execution Environment1", value = "이 봇은 Galaxy S8+ with Termux and Pixel experience로 동작중입니다. (24h Server)", inline = False)
        embed.add_field(name = "Execution Environment2", value = "현재, 이 봇은 LG 울트라북 15U560에서 동작중입니다. (Developing Server)", inline = False)
        embed.add_field(name = "Helper_Slack bot", value = "Koi_Bot이 Slack Bot인 시절에 도와주신 bright_minary님, name10님, hotmandu님에게 감사드립니다.", inline = False)
        embed.add_field(name = "Helper_Discord bot", value = "코드 개발에 도움을 주시고, 컴파일 함수의 아이디어를 제공해주신 tmvkrpxl0님에게 감사드립니다.", inline = False)
        embed.add_field(name = "Reference Document", value = "이 봇은 이를 참조/사용하여 제작되었습니다.\n키뮤님의 Setabot Framework : https://github.com/Kimu-Nowchira/SetaBot\n곰사냥님의 디스코드 봇 만들기 문서 : https://blog.naver.com/huntingbear21/221646735340", inline = False)
        await ctx.reply(embed=embed, mention_author = False)                                  

def setup(app):
    app.add_cog(BotManagement(app))
