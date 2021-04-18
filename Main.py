import discord
from discord.ext import commands

import os

from Config import Config
from Utils import Logger

cog_list = []
app = commands.Bot(command_prefix = "//")
app.remove_command("help")

def get_token(): # Get tokens from key.key
    with open("Key.key", "r") as f:
        return f.readline().strip()

@app.event # Statement changing
async def on_ready():
    Logger.info("Logining to : " + str(app.user.name) + "(code : " + str(app.user.id) + ")")
    game = discord.Game("Running.........")
    await app.change_presence(status=discord.Status.online, activity=game)
    Logger.info("Bot is started!")

for filename in os.listdir("Cogs"): # Get all Cogs from Cogs folder
    if filename.endswith(".py"):
        app.load_extension(f"Cogs.{filename[:-3]}")
        cog_list.append(filename[:-3])

@app.command(name="load")
async def load_commands(ctx, extension):
    if ctx.author.id not in Config.admin_id:
        embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
        await ctx.reply(embed = embed, mention_author = False)
        return

    app.load_extension(f"Cogs.{extension}")
    await ctx.reply(f"{extension} is loaded successfully!")
    cog_list.append(extension)

@app.command(name="unload")
async def unload_commands(ctx, extension):
    if ctx.author.id not in Config.admin_id:
        embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
        await ctx.reply(embed = embed, mention_author = False)
        return

    app.unload_extension(f"Cogs.{extension}")
    await ctx.reply(f"{extension} is unloaded successfully!")
    cog_list.remove(extension)

@app.command(name="reload")
async def reload_commands(ctx, extension=None):
    if ctx.author.id not in Config.admin_id:
        embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
        await ctx.reply(embed = embed, mention_author = False)
        return

    if extension is None:
        cog_list_tmp = list(cog_list)
        cnt = 0
        msg = await ctx.reply(f"Reloading Extension... {cnt}/{len(cog_list)} Reloaded!")
        for extension in cog_list_tmp:
            await msg.edit(content = f"Reloading Extension... {cnt}/{len(cog_list)} Reloaded!\nNow reloading {extension} extension!")
            app.unload_extension(f"Cogs.{extension}")
            cog_list.remove(extension)
            app.load_extension(f"Cogs.{extension}")
            cog_list.append(extension)
            cnt = cnt+1
        await msg.edit(content = f"Reloading Extension... {cnt}/{len(cog_list)} Reloaded!\nAll extension reloaded successfully!")
    else: 
        app.unload_extension(f"Cogs.{extension}")
        cog_list.remove(extension)
        app.load_extension(f"Cogs.{extension}")
        cog_list.append(extension)
        await ctx.reply(f"{extension} is reloaded successfully!")

@app.command(name = "help") # Help command
async def help_command(ctx,func = None):
    if func is None:
        embed = discord.Embed(title="Koi_Bot 도움말", description="명령 구문은 //`명령어` 입니다.", color=0x00ffff) 
        embed.set_footer(text="//help `명령어`로 특정 명령어의 자세한 설명을 보실 수 있습니다!")
        for x in cog_list:
            if str(x) == "BotEvent":
                continue
            cog_data = app.get_cog(x)
            command_list = cog_data.get_commands()
            embed.add_field(name=x, value=" ".join([c.name for c in command_list]), inline=False) 
        await ctx.reply(embed=embed, mention_author = False)
    else:
        command_notfound = True
        for _title, cog in app.cogs.items():
            if not command_notfound:
                break

            else:
                if func == "compile": # Process compile command
                    cmd = app.get_command("compile")
                    embed = discord.Embed(title=f"명령어 : {cmd}", description=cmd.help, color=0x00ffff)
                    embed.set_footer(text="//help `명령어`로 특정 명령어의 자세한 설명을 보실 수 있습니다!")
                    embed.add_field(name = "사용법",value = "아래의 사진을 참고해 주세요.")
                    embed.set_image(url="https://cdn.discordapp.com/attachments/743278669665009694/759765708250546246/asdfasdf.PNG")
                    await ctx.reply(embed=embed, mention_author = False)
                    command_notfound = False
                else:
                    for title in cog.get_commands():
                        if title.name == func:
                            cmd = app.get_command(title.name)
                            embed = discord.Embed(title=f"명령어 : {cmd}", description=cmd.help, color=0x00ffff)
                            embed.set_footer(text="//help `명령어`로 특정 명령어의 자세한 설명을 보실 수 있습니다!")
                            embed.add_field(name="사용법", value=cmd.usage)
                            await ctx.reply(embed=embed, mention_author = False)
                            command_notfound = False
                            break
                        else:
                            command_notfound = True
        
        if command_notfound:
            if func in cog_list:
                cog_data = app.get_cog(func)
                command_list = cog_data.get_commands()
                embed = discord.Embed(title=f"Category : {cog_data.qualified_name}", description=cog_data.description, color=0x00ffff)
                embed.set_footer(text="//help `명령어`로 특정 명령어의 자세한 설명을 보실 수 있습니다!")
                for c in command_list:
                    cmd = app.get_command(c.name)
                    embed.add_field(name=cmd.name, value=cmd.help, inline = False)
                await ctx.reply(embed=embed, mention_author = False)
            else:
                await ctx.reply("그런 이름의 명령어나 카테고리는 없습니다.", mention_author = False)


app.run(get_token())