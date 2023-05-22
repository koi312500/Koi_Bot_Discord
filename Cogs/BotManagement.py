import discord
import asyncio
from discord.commands import permissions
from discord.ext import commands
from discord.ext import tasks
from discord.commands import slash_command

import time
import subprocess
import platform

from config import Slash_Command_Server as SCS
from Utils import Permission
from Utils import Logger

class BotManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status_change.start()

    @tasks.loop(seconds = 30)
    async def status_change(self):
        await self.bot.wait_until_ready()
        status_list = ["Made by KOI#4182. (Ver.1)", "`/invite` to join KOI Server!"]
        for i in status_list:
            await asyncio.sleep(15)
            await self.bot.change_presence(status = discord.Status.online, activity = discord.Game(i))
    
    @slash_command(name = "update_delay", guild_ids = SCS)
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
        

    @slash_command(name = "restart", guild_ids = SCS)
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

    @slash_command(name = "stop", guild_ids = SCS)
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

        await ctx.respond("'Koi_Bot#4999'의 초대 링크 : https://discord.com/oauth2/authorize?client_id=905845362344996874&scope=bot%20applications.commands\n'Hello, Discord!' 서버(코이 서버)의 초대링크 : https://discord.gg/sX2K7eGdzT", ephemeral = True)

    @slash_command(name = "info")
    async def info_command(self,ctx):
        if await Permission.check_permission(ctx, 1):
            return None
          
        embed = discord.Embed(title=f"Koi_Bot Info", color=0x0AB1C2)
        embed.set_footer(text=f"현재 봇의 버전은 Alpha v_4 입니다.")
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
