import discord
import asyncio
from discord.commands import permissions
from discord.ext import commands
from discord.ext import tasks
from discord.commands import slash_command

import time
import subprocess
import platform

from Utils import Permission
from Utils import Logger

class BotManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status_change.start()

    @tasks.loop(seconds = 30)
    async def status_change(self):
        status_list = ["Made by KOI#4182. (Alpha v_2)", "Changing Library from dpy to pycord. (Alpha v_2)"]
        for i in status_list:
            await asyncio.sleep(15)
            await self.bot.change_presence(status = discord.Status.online, activity = discord.Game(i))
    
    @slash_command(name = "update_delay", guild_ids = [742201063972667487])
    @permissions.has_any_role("Owner")
    async def update_delay_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
        await Logger.info("1H Server stop for update is requested.", self.bot)
        if str(platform.system()) == "Windows":
            await ctx.respond("Execution platform is **Windows**. Update_delay system for **Windows** is deleted by owner. No action.")
            await Logger.info("No action because execution platform is Windows.", self.bot)
        elif str(platform.system()) == "Linux":
            await ctx.respond("Execution platform is **Linux**, Request to start update_delay.sh.")
            subprocess.call("./update_delay.sh &", shell = True)
            await Logger.info("Shell command './update_delay.sh &' is requested.", self.bot)
            await Logger.info("Exiting progress.", self.bot)
            await asyncio.sleep(3)
            await ctx.respond("Done. Exiting progress.")
            exit()
        else:
            Logger.info("Cannot detect execution platform. Cannot update automatically.",self.bot)
            await ctx.respond("Cannot detect your execution platform. Cannot reboot your bot automatically.", self.bot)
        

    @slash_command(name = "restart", guild_ids = [742201063972667487])
    @permissions.has_any_role("Owner")
    async def restart_command(self,ctx):
        if await Permission.check_permission(ctx, 3):
            return None
          
        await Logger.info("Restarting is requested.", self.bot)
        if str(platform.system()) == "Windows":
            await ctx.respond("Execution platform is **Windows**. Reboot system for **Windows** is deleted by owner. No action.")
            await Logger.info("No action because execution platform is Windows.", self.bot)
        elif str(platform.system()) == "Linux":
            await ctx.respond("Execution platform is **Linux**, Request to start restart.sh.")
            subprocess.call("./restart.sh &", shell = True)
            await Logger.info("Shell command './restart.sh &' is requested.", self.bot)
            await Logger.info("Exiting progress.", self.bot)
            await asyncio.sleep(3)
            await ctx.respond("Done. Exiting progress.")
            exit()
        else:
            Logger.info("Cannot detect execution platform. Cannot update automatically.",self.bot)
            await ctx.respond("Cannot detect your execution platform. Cannot reboot your bot automatically.", self.bot)

    @slash_command(name = "stop", guild_ids = [742201063972667487])
    @permissions.has_any_role("Owner")
    async def stop_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None
          
        await Logger.info("Exiting progress.", self.bot)
        await ctx.respond("Exiting progress.")
        exit()
   
    @slash_command(name = "invite")
    async def invite_server_command(self, ctx):
        if await Permission.check_permission(ctx, 1):
            return None

        await ctx.author.send("봇 서버 링크는 다음과 같습니다.")
        await ctx.author.send("https://discord.gg/sX2K7eGdzT")
        await ctx.respond("Koi_Bot의 공식 서버 초대 링크가 DM으로 전송되었습니다!")

    @slash_command(name = "info")
    async def info_command(self,ctx):
        if await Permission.check_permission(ctx, 1):
            return None
          
        embed = discord.Embed(title=f"Koi_Bot Info", color=0x00ffff)
        embed.set_footer(text=f"현재 봇의 버전은 Alpha v_2 입니다.")
        embed.add_field(name = "Owner/Maker", value = "이 봇은 KOI#4182 에 의해 제작되었습니다.", inline = False)
        embed.add_field(name = "License", value = "이 봇은 MIT 라이센스를 따르고 있습니다.", inline = False)
        embed.add_field(name = "Execution Environment1", value = "이 봇은 Galaxy S8+ with Termux and Pixel experience로 동작중입니다. (24h Server)", inline = False)
        embed.add_field(name = "Execution Environment2", value = "이 봇은 Samsung Galaxy Book Ion 2 에서 동작중입니다. (Developing Server)", inline = False)
        embed.add_field(name = "Helper_Slack bot", value = "Koi_Bot이 Slack Bot인 시절에 도와주신 bright_minary님, name10님, hotmandu님에게 감사드립니다.", inline = False)
        embed.add_field(name = "Helper_Discord bot", value = "코드 개발에 도움을 주시고, 컴파일 함수의 아이디어를 제공해주신 tmvkrpxl0님에게 감사드립니다.", inline = False)
        embed.add_field(name = "Reference Document", value = "이 봇은 이를 참조/사용하여 제작되었습니다.\n1. 키뮤님의 Setabot Framework : https://github.com/Kimu-Nowchira/SetaBot", inline = False)
        await ctx.respond(embed=embed)                                  

def setup(bot):
    bot.add_cog(BotManagement(bot))
