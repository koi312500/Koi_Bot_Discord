from discord.ext import commands
import discord

import time
import random

import config
from Utils import Logger
from Utils.UserClass import UserClass as User
cooldown = {}

class BotEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg): # Give XP to all message.
        member = User(msg.author.id)
        global cooldown
        if member.id in cooldown:
            if time.time() - cooldown[member.id] < 60:
                return

        cooldown[member.id] = time.time()
        member.add_exp(random.randint(15, 25))
        
        

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        Logger.err(error)  # Logging the error using the Logger utility

        error_notfound = True
        
        # Handling MissingPermissions error
        if isinstance(error, commands.errors.MissingPermissions):
            error_notfound = False
            embed = discord.Embed(
                title=f"이 명령어를 {ctx.author}의 권한 부족으로 실행하지 못했습니다.",
                description="관리자에게 권한 추가를 요청해 보세요.",
                color=0xff0000
            )
        
        try:
            # Handling errors related to Forbidden (lack of bot's permissions)
            if isinstance(error.original, discord.Forbidden):
                error_notfound = False
                embed = discord.Embed(
                    title=f"이 명령어를 {config.bot_name}의 권한 부족으로 실행하지 못했습니다.",
                    description="관리자에게 권한 추가를 요청해 보세요.",
                    color=0xff0000
                )
        except:
            pass
    
        # Handling other errors not specified above
        if error_notfound == True:
            embed = discord.Embed(
                title="Error Info",
                description=f"{config.bot_name} Error Info",
                color=0xff0000
            )
            embed.add_field(name="Error Info", value=f"```{error}```")
        
        await ctx.respond(embed=embed)  # Responding with an embedded message indicating the error

# Function to set up the cog
def setup(bot):
    bot.add_cog(BotEvent(bot))
