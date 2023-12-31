import discord
from discord.ext import commands

import config
from Utils.UserClass import UserClass as User  # Importing the UserClass from Utils module

# List containing permission messages for different levels
permission_message = [
    "Guest [Permission Level : 0]",
    "User [Permission Level : 1]",
    "Developer [Permission Level : 2]",
    "Owner [Permission Level : 3]"
]

# Async function to check user permission against a given level
async def check_permission(ctx, level):
    now_user = User(ctx.author)  # Creating an instance of UserClass with the author from the context
    if now_user.permission >= level:  # Checking if the user's permission level is greater than or equal to the required level
        return False  # User has sufficient permission
    else:
        # Creating an embed to display permission error message
        embed = discord.Embed(title=f"User Permission Error", color=0xff0000)
        embed.set_footer(text=f"Sent by {config.bot_name}ㆍUser Permission Error")
        
        # Handling different permission cases with specific messages
        if now_user.permission == 0 and level == 1:
            embed.add_field(
                name="Suggestion",
                value=f"/accept_term으로 약관 동의를 하시면, `{permission_message[1]}` 권한을 얻어, 이 명령어를 실행 하실 수 있습니다.",
                inline=False
            )
        
        embed.add_field(
            name="Your Permission",
            value=f"{str(permission_message[int(now_user.permission)])}",
            inline=True
        )
        embed.add_field(
            name="Command Executable Permission",
            value=f"{str(permission_message[int(level)])}",
            inline=True
        )
        
        await ctx.respond(embed=embed)  # Sending the embed message indicating permission error
        return True  # User doesn't have sufficient permission
