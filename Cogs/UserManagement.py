import discord
import asyncio
from discord.ext import commands
from discord.commands import permissions
from discord.commands import slash_command

import config
from config import Slash_Command_Server as SCS
from Utils import Permission
from Utils import Logger
from Utils.UserClass import UserClass as User

class UserManagement(commands.Cog):
    def __init__(self, app):
        self.app = app
    
    class MyView(discord.ui.View):
        async def on_timeout(self):
            await self.message.edit(view=self)

        @discord.ui.button(label = "동의합니다", style=discord.ButtonStyle.primary, emoji="⭕")
        async def first_button_callback(self, button, interaction):
            permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
            now_user = User(interaction.user)
            for child in self.children:
                child.disabled = True
            content = f"{config.bot_name} 의 약관에 동의하셨습니다!\n"
            content = content + f"Permission이 '{str(permission_message[int(now_user.permission)])}' 에서, 'User [Permission Level : 1]' 으로 변경됩니다.\n"
            await self.message.edit(view=self)
            await interaction.response.send_message(content = content)
            if now_user.permission <= 1:
                now_user.permission = 1

        @discord.ui.button(label = "동의하지 않습니다", style=discord.ButtonStyle.primary, emoji="❌")
        async def second_button_callback(self, button, interaction):
            for child in self.children:
                child.disabled = True
            await self.message.edit(view=self)  
            await interaction.response.send_message(content = f"{config.bot_name} 의 약관에 동의하지 않으셨습니다. {config.bot_name}의 기능을 사용하기 위해서는, 약관에 동의해주셔야 합니다.")

    @slash_command(name = "accept_term", guild_ids = SCS)
    async def AcceptTerm_command(self, ctx):
        permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
        now_user = User(ctx.author)
        embed = discord.Embed(title=f"{config.bot_name} 약관", color=0x0AB1C2)
        embed.set_footer(text=f"Sented by {config.bot_name}ㆍaccept_term Command's Result")
        embed.add_field(name = "Term1", value = f"{config.bot_name}을 사용하시면서, 발생하는 모든 메세지 기록이 특별한 명시 없이 저장되는 것이 허용됩니다.", inline = False)
        embed.add_field(name = "Term2", value = f"{config.bot_name}에 당신의 Discord Nickname, ID가 제공됩니다.", inline = False)
        embed.add_field(name = "Result", value = f"Permission이 '{str(permission_message[int(now_user.permission)])}' 에서, 'User [Permission Level : 1]' 으로 변경됩니다.", inline = False)
        embed.add_field(name = "How to Agree", value = f":o: 반응을 추가함으로써, 약관에 동의하실 수 있습니다.", inline = False)
        message = await ctx.respond(embed = embed, view=self.MyView(timeout=15))

    @commands.has_permissions(manage_messages = True)
    @slash_command(name = "set_permission", guild_ids = SCS)
    async def SetPermission_command(self, ctx, command_user: discord.User, value1):
        if await Permission.check_permission(ctx, 3):
            return None
        permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
        now_user = User(command_user)
        now_user.permission = value1
        await ctx.respond(f"{str(now_user.name)} 님의 권한이 '{str(permission_message[int(now_user.permission)])}' 으로 설정되셨습니다!")

    @slash_command(name = "user")
    async def myinfo_show_command(self, ctx, command_user : discord.User = None):
        if await Permission.check_permission(ctx, 1):
            return None
        permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
        if command_user == None:
            now_user = User(ctx.author)
        else:
            now_user = User(command_user)
        embed = discord.Embed(title=f"{str(now_user.name)} 님의 {config.bot_name} Info", color=0x0AB1C2)
        embed.set_footer(text = f"Sented by {config.bot_name}ㆍuser Command's Result")
        embed.add_field(name = f"현재 레벨", value = f"{now_user.level}레벨, {now_user.exp} exp를 가지고 있어요! ", inline = False)
        embed.add_field(name = f"Permission", value = f"현재 권한 등급 : {str(permission_message[int(now_user.permission)])}")
        await ctx.respond(embed=embed)  

def setup(app):
    app.add_cog(UserManagement(app)) 