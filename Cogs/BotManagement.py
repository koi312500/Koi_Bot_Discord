import discord
import asyncio
from discord.ext import commands

import subprocess
import platform

from Utils import Logger
from Config import Config

class BotManagement(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "restart", help = "봇을 재부팅하고, 업데이트 코드를 확인합니다.", usage = "관리자용 커맨드입니다.")
    async def restart_command(self,ctx):
        if ctx.author.id not in Config.admin_id:
            embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
            await ctx.reply(embed = embed, mention_author = False)
            return

        Logger.info("Restarting is requested.")
        if str(platform.system()) == "Windows":
            await ctx.reply("Execution platform is **Windows**, Request to start update.bat.")
            subprocess.call("start update.bat ",shell = True)
            Logger.info("Shell command 'start update.bat' is requested.")
        elif str(platform.system()) == "Linux":
            await ctx.reply("Execution platform is **Linux**, Request to start update.sh.")
            subprocess.call("./update.sh &", shell = True)
            Logger.info("Shell command './update.sh &' is requested.")
        else:
            Logger.info("Cannot detect execution platform. Cannot update automatically.")
            await ctx.reply("Cannot detect your execution platform. Cannot update your bot automatically.")
        Logger.info("Exiting progress.")
        await asyncio.sleep(3)
        await ctx.reply("Done. Exiting progress.")
        exit()

    @commands.command(name = "stop", help = "봇을 종료합니다.", usage = "관리자용 커맨드입니다.")
    async def stop_command(self, ctx):
        if ctx.author.id not in Config.admin_id:
            embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
            await ctx.reply(embed = embed, mention_author = False)
            return

        Logger.info("Exiting progress.")
        await ctx.reply("Exiting progress.")
        exit()
   
    @commands.command(name = "invite", help = "Koi_Bot의 공식 서버 초대 링크를 보내드립니다.", usage = "//invite")
    async def invite_server_command(self, ctx):
        await ctx.author.send("봇 서버 링크는 다음과 같습니다.")
        await ctx.author.send("https://discord.gg/sX2K7eGdzT")
        await ctx.reply("Koi_Bot의 공식 서버 초대 링크가 DM으로 전송되었습니다!", mention_author = False)

    @commands.command(name = "info", help = "Koi_Bot의 정보를 출력합니다.", usage = "//info")
    async def info_command(self,ctx):
        embed = discord.Embed(title=f"Koi_Bot Info", color=0x00ffff)
        embed.set_footer(text=f"현재 봇의 버전은 {Config.version} 입니다.")
        embed.add_field(name = "Owner/Maker", value = "이 봇은 AKMU_LOVE#4211에 의해 제작되었습니다.", inline = False)
        embed.add_field(name = "License", value = "이 봇은 MIT License를 따르고 있습니다.", inline = False)
        #embed.add_field(name = "Execution Environment", value = "현재, 이 봇은 Galaxy S8+ with Termux and Pixel experience로 동작중입니다.", inline = False)
        embed.add_field(name = "Execution Environment", value = "현재, 이 봇은 LG 울트라북 15U560에서 동작중입니다.", inline = False)
        embed.add_field(name = "Helper_Slack bot", value = "Koi_Bot이 Slack Bot인 시절에 도와주신 bright_minary님, name10님, hotmandu님에게 감사드립니다.", inline = False)
        embed.add_field(name = "Helper_Discord bot", value = "코드 개발에 도움을 주시고, 컴파일 함수의 아이디어를 제공해주신 tmvkrpxl0님에게 감사드립니다.", inline = False)
        embed.add_field(name = "Reference Document", value = "이 봇은 이를 참조/사용하여 제작되었습니다.\n키뮤님의 Setabot Framework : https://github.com/Kimu-Nowchira/SetaBot\n곰사냥님의 디스코드 봇 만들기 문서 : https://blog.naver.com/huntingbear21/221646735340", inline = False)
        await ctx.reply(embed=embed, mention_author = False)                                  

def setup(app):
    app.add_cog(BotManagement(app))