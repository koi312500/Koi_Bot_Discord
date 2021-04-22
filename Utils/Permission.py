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
        embed.add_field(name = "Your Permission", value = f"{str(permission_message[int(now_user.permission)])}", inline = True)
        embed.add_field(name = "Command Executable Permission", value = f"{str(permission_message[int(level)])}", inline = True)
        await ctx.reply(embed=embed, mention_author = False)        
        return True