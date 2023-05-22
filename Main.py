import discord
from discord.ext import commands
from discord.commands import permissions

import os

from config import Slash_Command_Server as SCS
import config
from Utils import Permission
from Utils import Logger

cog_list = []
bot = discord.Bot()

@bot.event # Statement changing
async def on_ready():
    await Logger.info("Login to : " + str(bot.user.name) + "(code : " + str(bot.user.id) + ")", bot)
    game = discord.Game("Running.........")
    await bot.change_presence(status=discord.Status.online, activity=game)
    await Logger.info("Bot is started!", bot)

for filename in os.listdir("Cogs"): # Get all Cogs from Cogs folder
    if filename.endswith(".py"):
        if filename.startswith("bak_"):
            continue
        bot.load_extension(f"Cogs.{filename[:-3]}")
        cog_list.append(filename[:-3])

@bot.slash_command(name="load", guild_ids = SCS)
async def load_commands(ctx, extension):    
    if await Permission.check_permission(ctx, 3):
        return None
    
    bot.load_extension(f"Cogs.{extension}")
    await ctx.respond(f"{extension} is loaded successfully!")
    cog_list.append(extension)
    await Logger.info(f"Extension {extension} is loaded.", bot)

@bot.slash_command(name="unload", guild_ids = SCS)
async def unload_commands(ctx, extension):
    if await Permission.check_permission(ctx, 3):
        return None

    bot.unload_extension(f"Cogs.{extension}")
    await ctx.respond(f"{extension} is unloaded successfully!")
    cog_list.remove(extension)
    await Logger.info(f"Extension {extension} is unloaded.", bot)

@bot.slash_command(name="reload", guild_ids = SCS)
async def reload_commands(ctx, extension=None):
    if await Permission.check_permission(ctx, 3):
        return None

    if extension is None:
        cog_list_tmp = list(cog_list)
        msg = await ctx.respond(f"Reloading all extensions...")
        for extension in cog_list_tmp:
            bot.unload_extension(f"Cogs.{extension}")
            cog_list.remove(extension)
            bot.load_extension(f"Cogs.{extension}")
            cog_list.append(extension)
        await msg.edit_original_response(content = f"All extensions are reloaded completely!")
        await Logger.info("All Extensions are reloaded.", bot)
    else: 
        bot.unload_extension(f"Cogs.{extension}")
        cog_list.remove(extension)
        bot.load_extension(f"Cogs.{extension}")
        cog_list.append(extension)
        await ctx.respond(f"{extension} is reloaded successfully!")
        await Logger.info(f"Extension {extension} is reloaded.", bot)


bot.run(config.discord_key)