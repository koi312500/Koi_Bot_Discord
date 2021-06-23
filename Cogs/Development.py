import discord
import asyncio
from discord.ext import commands
import subprocess
import platform
import datetime
import inspect

from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User

class Development(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def test_command(self, ctx, value_tmp):
        if await Permission.check_permission(ctx, 3):
            return None
        await ctx.reply("Hello, World!")

def setup(app):
    app.add_cog(Development(app))