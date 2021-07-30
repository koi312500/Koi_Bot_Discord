import discord
from discord import user
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.model import ButtonStyle

from Utils import Permission

class Slash(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name = "slash", help = "디스코드의 기능을 활용한 Slash Command의 사용법 및 목록을 설명합니다.", usage = "//slash")
    async def slash_command(self, ctx):
        await ctx.reply("Slash Command의 경우 `/`를 채팅창에 치면 사용 가능합니다! Slash Command의 목록에는 현재 `SlashTest` 의 총 1개의 명령어가 존재합니다.", mention_author = False)
    
    @cog_ext.cog_slash(name="SlashTest",
             description="단순한 SlashCommand Test입니다.",
             options=[
               create_option(
                 name="optone",
                 description="This is the first option we have.",
                 option_type=3,
                 required=False
               )
             ])
    async def SlashTest_SlashCommand(self, ctx, optone = None):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])
        await ctx.send(f"You send the optone {optone}")
        if optone is not None:
            print(optone)
            await ctx.send(f"You send the optone {optone}")

    @cog_ext.cog_slash(name="delete",
             description="너가 만든 쓰레기를 청소한다",
             options=[
               create_option(
                 name="amount",
                 description="너가 만든 쓰레기의 양",
                 option_type=4,
                 required=True
               )
             ])
    async def delete_SlashCommand(self, ctx, amount : int):
      if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit = int(amount))
        await ctx.send(f"{amount} message was deleted.")
      else:
        await ctx.send("You don't have permission to delete all text.")

    @cog_ext.cog_slash(name="ban",
             description="너를 차고 나서 문을 닫아버릴거다",
             options=[
               create_option(
                 name="user_name",
                 description="너가 차고 싶은 사람",
                 option_type=6,
                 required=True
               )
             ])
    async def ban_SlashCommand(self, ctx, user_name : discord.Member):
      if ctx.author.guild_permissions.ban_members:
        await user_name.ban()
        await ctx.send(f"{user_name} was baned.")
      else:
        await ctx.send("You don't have permission to ban somebody.")



def setup(app):
    app.add_cog(Slash(app))