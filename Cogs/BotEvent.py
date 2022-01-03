from discord.ext import commands
import discord

from Utils import Logger

class BotEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        Logger.err(error)
        error_notfound = True
        
        if isinstance(error, commands.errors.MissingPermissions):
            error_notfound = False
            embed = discord.Embed(title = f"이 명령어를 {ctx.author} 의 권한 부족으로 실행하지 못했습니다.", description = "관리자에게 권한 추가를 요청해 보세요.", color = 0xff0000)
        
        try:
            if isinstance(error.original, discord.Forbidden):
                error_notfound = False
                embed = discord.Embed(title = f"이 명령어를 Koi_Bot#4999 의 권한 부족으로 실행하지 못했습니다.", description = "관리자에게 권한 추가를 요청해 보세요.", color = 0xff0000)
        except:
            pass
    
        if error_notfound == True:
            embed = discord.Embed(title="Error Info", description="Koi_Bot Error Info", color=0xff0000)
            embed.add_field(name="Error Info", value=f"```{error}```")
        
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(BotEvent(bot)) 