import discord
import asyncio
from discord.ext import commands

from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User

class UserManagement(commands.Cog):
    def __init__(self, app):
        self.app = app
        
    @commands.command(name = "AcceptTerm")
    async def AcceptTerm_command(self, ctx):
        permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
        now_user = User(ctx.author)
        embed = discord.Embed(title=f"Koi_Bot 약관", color=0x00ffff)
        embed.set_footer(text="Sented by Koi_Bot#7938ㆍAcceptTerm Command's Result")
        embed.add_field(name = "Term1", value = "Koi_Bot#7938을 사용하시면서, 발생하는 모든 메세지 기록이 특별한 명시 없이는 저장되는 것이 허용됩니다.", inline = False)
        embed.add_field(name = "Term2", value = "Koi_Bot#7938, AKMU_LOVE#4211(KOI#4182)등의 개발자에게 당신의 Discord Nickname, ID가 제공됩니다.", inline = False)
        embed.add_field(name = "Result", value = f"Permission이 '{str(permission_message[int(now_user.permission)])}' 에서, 'User [Permission Level : 1]' 으로 변경됩니다.", inline = False)
        embed.add_field(name = "How to Agree", value = ":o: 반응을 추가함으로써, 약관에 동의하실 수 있습니다.", inline = False)
        message = await ctx.reply(embed = embed, mention_author = False)
        await message.add_reaction("⭕")
        await message.add_reaction("❌")
        reaction_list = ['⭕', '❌']
        for r in reaction_list:
            await message.add_reaction(r)
        def check(reaction, user):
            return str(reaction) in reaction_list and user == ctx.author and reaction.message.id == message.id
        try:
            reaction, _user = await self.app.wait_for("reaction_add", check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.reply("시간 초과되었습니다.", mention_author = False)
        else:
            if str(reaction) == '⭕':
                await ctx.reply("Koi_Bot#7938 의 약관에 동의하셨습니다! ", mention_author = False)
                await ctx.reply(f"Permission이 '{str(permission_message[int(now_user.permission)])}' 에서, 'User [Permission Level : 1]' 으로 변경됩니다.", mention_author = False)
                now_user.permission = 1
            else:
                await ctx.reply("Koi_Bot#7938의 약관에 동의하지 않으셨습니다.", mention_author = False)

    @commands.command(name = "SetPermission")
    async def SetPermission_command(self, ctx, command_user: discord.User, value1):
        if await Permission.check_permission(ctx, 3):
            return None
        permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
        now_user = User(command_user)
        now_user.permission = value1
        await ctx.reply(f"{str(now_user.name)} 님의 권한이 '{str(permission_message[int(now_user.permission)])}' 으로 설정되셨습니다!")

    @commands.command(name = "user")
    async def myinfo_show_command(self, ctx, command_user : discord.User = None):
        permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
        if command_user == None:
            now_user = User(ctx.author)
        else:
            now_user = User(command_user)
        embed = discord.Embed(title=f"{str(now_user.name)} 님의 Koi_Bot Info", color=0x00ffff)
        embed.set_footer(text="//me 명령어의 결과입니다.")
        embed.add_field(name = "현재 레벨", value = f"{now_user.level}레벨, {now_user.exp} exp를 가지고 있어요! ", inline = False)
        embed.add_field(name = "Permission", value = f"현재 권한 등급 : {str(permission_message[int(now_user.permission)])}")
        await ctx.reply(embed=embed, mention_author = False)  

def setup(app):
    app.add_cog(UserManagement(app)) 