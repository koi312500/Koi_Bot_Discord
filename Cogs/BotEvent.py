from discord.ext import commands
import discord

from Utils import Logger

class BotEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        Logger.info(f"Entered to '{guild.name}' Server.", self.bot)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        Logger.info(f"Kicked from '{guild.name}' Server.", self.bot)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        Logger.err(error)
        error_notfound = True

        if isinstance(error, commands.CommandNotFound):
            error_notfound = False
            embed = discord.Embed(title = "그런 커맨드는 존재하지 않습니다.", description = "//help 로 어떤 명령어가 있는지 확인하실 수 있습니다.", color = 0xff0000)
        
        if isinstance(error, commands.MissingRequiredArgument):
            error_notfound = False
            embed = discord.Embed(title = "인자가 입력되지 않았습니다.", description = f"`//help {ctx.command}` 로 {ctx.command} 명령어의 사용법을 확인하실 수 있습니다.", color = 0xff0000)
        
        if isinstance(error, commands.BadArgument):
            error_notfound = False
            embed = discord.Embed(title = "잘못된 인자가 입력되었습니다.", description = f"`//help {ctx.command}` 로 {ctx.command} 명령어의 사용법을 확인하실 수 있습니다.", color = 0xff0000)
        
        if isinstance(error, commands.errors.MissingPermissions):
            error_notfound = False
            embed = discord.Embed(title = f"이 명령어를 {ctx.author} 의 권한 부족으로 실행하지 못했습니다.", description = "관리자에게 권한 추가를 요청해 보세요.", color = 0xff0000)
        
        if error_notfound == True:
            embed = discord.Embed(title="Error Info", description="Koi_Bot Error Info", color=0xff0000)
            embed.add_field(name="Error Info", value=f"```{error}```")
        
        try:
            await ctx.respond(embed=embed)
        except discord.errors.Forbidden:
            ctx.author.send(embed=embed)
            ctx.author.send("서버에 메세지를 보낼 수가 없어요. 권한을 확인해주세요.")

def setup(bot):
    bot.add_cog(BotEvent(bot)) 