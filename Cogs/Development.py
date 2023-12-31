import discord
from discord.ext import commands
from discord.commands import slash_command

import random
import subprocess

# Importing configuration and utilities
import config
from config import Slash_Command_Server as SCS
from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User

class Development(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Command for testing purposes
    @slash_command(name="test", guild_ids=SCS)
    async def test_command(self, ctx):
        if await Permission.check_permission(ctx, 2):
            return None
        embed = discord.Embed(
            title=f'/test {config.bot_name} Slash Result',
            description='Test Succeed. Result printed.',
            color=0x00ffff
        )
        embed.add_field(
            name="Embed's purpose",
            value=f"To test {config.bot_name}'s Slash Command.",
            inline=False
        )
        await ctx.respond(embed=embed)

    # Command for updating bot from remote
    @slash_command(name="update", guild_ids=SCS)
    async def update_command(self, ctx):
        if await Permission.check_permission(ctx, 2):
            return None
        msg = await ctx.respond(f"/update Started. Wait for a second...")
        embed = discord.Embed(
            title='Update command Result',
            description='Remote update',
            color=0x00ffff
        )
        # Pulling changes from the git repository
        fd_popen = subprocess.Popen("git pull origin master", shell=True, stdout=subprocess.PIPE).stdout
        command_data = fd_popen.read().strip()
        fd_popen.close()
        if len(command_data) > 1024:
            command_data = command_data[-700:]
        embed.add_field(
            name="Result of the `git pull origin master`",
            value=command_data,
            inline=False
        )
        # Installing required dependencies
        fd_popen = subprocess.Popen("pip install -r requirements.txt", shell=True, stdout=subprocess.PIPE).stdout
        command_data = fd_popen.read().strip()
        fd_popen.close()
        if len(command_data) > 1024:
            command_data = command_data[-700:]
        embed.add_field(
            name="Result of the `pip install -r requirements.txt`",
            value=command_data,
            inline=False
        )
        embed.set_footer(text=f"Sented by {config.bot_name}ㆍUpdate Command")
        await msg.edit_original_response(content="", embed=embed)
        await Logger.info("update command is activated", self.bot)

    # Command for giving XP to users
    @slash_command(name="givexp")
    async def GiveXP_command(self, ctx):
        if await Permission.check_permission(ctx, 1):
            return None
        now_user = User(ctx.author)
        x, y = random.randint(1, 25), random.randint(1, 25)
        if y == 25:
            now_user.add_exp(x * 1000)
            await ctx.respond(f"4% 당첨! XP를 {x * 1000}만큼 획득해서, {now_user.exp}의 xp를 보유중이에요!")
        else:
            now_user.add_exp(x)
            await ctx.respond(f"XP를 {x}만큼 획득해서, {now_user.exp}의 xp를 보유중이에요!", ephemeral=True)

def setup(app):
    app.add_cog(Development(app))
