import discord
from discord.ext import commands

from Utils.UserClass import UserClass as User

permission_message = ["Guest [Permission Level : 0]", "User [Permission Level : 1]", "Developer [Permission Level : 2]", "Owner [Permission Level : 3]"]
async def check_permission(ctx, level):
    now_user = User(ctx.author)
    if now_user.permission >= level:
        return False
    else:
        embed = discord.Embed(title=f"User Permission Error", color=0xff0000)
        embed.set_footer(text = "Sented by Koi_Bot#4999ㆍUser Permission Error")
        if now_user.permission == 0 and level == 1:
            embed.add_field(name = "Suggestion", value = "/accept_term으로 약관 동의를 하시면, 'User [Permission Level : 1]' 권한을 얻어, 이 명령어를 실행 하실 수 있습니다.", inline = False)
        embed.add_field(name = "Your Permission", value = f"{str(permission_message[int(now_user.permission)])}", inline = True)
        embed.add_field(name = "Command Executable Permission", value = f"{str(permission_message[int(level)])}", inline = True)
        await ctx.respond(embed=embed)        
        return True