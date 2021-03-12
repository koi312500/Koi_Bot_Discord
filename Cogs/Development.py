import discord
from discord.ext import commands
import subprocess
import platform
import datetime
import inspect

from Config import Config
from Utils import Logger
class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx, *, value_tmp):
        if ctx.author.id not in Config.admin_id:
            embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
            await ctx.reply(embed = embed, mention_author = False)
            return
        await ctx.message.delete()
        await ctx.send(str(value_tmp), mention_author = False)                                

    @commands.command()
    async def exec(self, ctx, *args):
        if ctx.author.id not in Config.admin_id:
            embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
            await ctx.reply(embed = embed, mention_author = False)
            return

        text = ' '.join(args)
        Logger.info(f'{str(ctx.author)}이(가) exec 명령어 사용 : {text}')
        result = exec(text)
        embed = discord.Embed(color=0x00FFFF, timestamp=datetime.datetime.today())
        if inspect.isawaitable(result):
            embed.add_field(name="🥚  **Exec**", value=f"```css\n[입구] {text}\n[출구] {await result}```", inline=False)
        else:
            embed.add_field(name="🥚  **Exec**", value=f"```css\n[입구] {text}\n[출구] {result}```", inline=False)
        embed.set_footer(text=f"{ctx.author.name} • exec", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=128)))
        await ctx.reply(embed=embed)

    @commands.command()
    async def eval(self, ctx, *args):
        if ctx.author.id not in Config.admin_id:
            embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
            await ctx.reply(embed = embed, mention_author = False)
            return

        text = ' '.join(args)
        Logger.info(f'{str(ctx.author)} used eval command : {text}')
        result = eval(text)
        embed = discord.Embed(color=0x00FFFF, timestamp=datetime.datetime.today())
        if inspect.isawaitable(result):
            embed.add_field(name="🥚  **Eval**", value=f"```css\n[입구] {text}\n[출구] {await result}```", inline=False)
        else:
            embed.add_field(name="🥚  **Eval**", value=f"```css\n[입구] {text}\n[출구] {result}```", inline=False)
        embed.set_footer(text=f"{ctx.author.name} • eval", icon_url=str(ctx.author.avatar_url_as(static_format='png', size=128)))
        await ctx.reply(embed=embed)

def setup(app):
    app.add_cog(Development(commands))