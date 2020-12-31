import asyncio
import discord
import os
import datetime
from discord.ext import commands
import sys
sys.path.insert(1, 'KoGPT2-chatbot')
import AI_talk as kogpt2

cog_list = []
app = commands.Bot(command_prefix = "//")
app.remove_command("help")

def get_token(): # Get tokens from key.key
    with open("Key.key", "r") as f:
        return f.readline().strip()

@app.event # Statement changing
async def on_ready():
    print("Logining to : " + str(app.user.name) + "(code : " + str(app.user.id) + ")")
    game = discord.Game("Running.........")
    await app.change_presence(status=discord.Status.online, activity=game)
    kogpt2.Load_Model() #Load Kogpt2 Model
    print("Bot is started!")

for filename in os.listdir("Cogs"): # Get all Cogs from Cogs folder
    if filename.endswith(".py"):
        app.load_extension(f"Cogs.{filename[:-3]}")
        cog_list.append(filename[:-3])

@app.command(name="load")
async def load_commands(ctx, extension):
    app.load_extension(f"Cogs.{extension}")
    await ctx.send(f"{extension} is loaded successfully!")
    cog_list.append(extension)

@app.command(name="unload")
async def unload_commands(ctx, extension):
    app.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"{extension} is unloaded successfully!")
    cog_list.remove(extension)

@app.command(name="reload")
async def reload_commands(ctx, extension=None):
    if extension is None:
        for extension in cog_list:
            app.unload_extension(f"Cogs.{extension}")
            app.load_extension(f"Cogs.{extension}")
            await ctx.send(f"{extension} is reloaded successfully!")
        await ctx.send("All extension is reloaded successfully!")
    else:
        app.unload_extension(f"Cogs.{extension}")
        app.load_extension(f"Cogs.{extension}")
        await ctx.send(f"{extension} is reloaded successfully!")

@app.command(name = "help") # Help command
async def help_command(ctx,func = None):
    if func is None:
        embed = discord.Embed(title="Koi_Bot 도움말", description="명령 구문은 //`명령어` 입니다.", color=0x00ffff) 
        embed.set_footer(text="//help `명령어`로 특정 명령어의 자세한 설명을 보실 수 있습니다!")
        for x in cog_list:
            cog_data = app.get_cog(x)
            command_list = cog_data.get_commands()
            embed.add_field(name=x, value=" ".join([c.name for c in command_list]), inline=True) 
        await ctx.send(embed=embed)
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
                    await ctx.send(embed=embed)
                    command_notfound = False
                else:
                    for title in cog.get_commands():
                        if title.name == func:
                            cmd = app.get_command(title.name)
                            embed = discord.Embed(title=f"명령어 : {cmd}", description=cmd.help, color=0x00ffff)
                            embed.set_footer(text="//help `명령어`로 특정 명령어의 자세한 설명을 보실 수 있습니다!")
                            embed.add_field(name="사용법", value=cmd.usage)
                            await ctx.send(embed=embed)
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
                embed.add_field(name="Commands", value=", ".join([c.name for c in command_list]))
                await ctx.send(embed=embed)
            else:
                await ctx.send("그런 이름의 명령어나 카테고리는 없습니다.")

@app.event
async def on_command_error(ctx, error):
    error_notfound = True
    if isinstance(error, commands.CommandNotFound):
        error_notfound = False
        embed = discord.Embed(title = "그런 커맨드는 존재하지 않습니다.", description = "//help 로 어떤 명령어가 있는지 확인하실 수 있습니다.", color = 0xff0000)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        error_notfound = False
        embed = discord.Embed(title = "인자가 입력되지 않았습니다.", description = f"`//help {ctx.command}` 로 {ctx.command} 명령어의 사용법을 확인하실 수 있습니다.", color = 0xff0000)
        await ctx.send(embed=embed)
    if isinstance(error, commands.BadArgument):
        error_notfound = False
        embed = discord.Embed(title = "잘못된 인자가 입력되었습니다.", description = f"`//help {ctx.command}` 로 {ctx.command} 명령어의 사용법을 확인하실 수 있습니다.", color = 0xff0000)
        await ctx.send(embed=embed)
    if isinstance(error, commands.BotMissingPermissions):
        error_notfound = False
        embed = discord.Embed(title = "봇이 이 명령어를 실행할 권한을 가지고 있지 않습니다.", description = "관리자에게 권한 추가를 요청해 보세요.", color = 0xff0000)
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        error_notfound = False
        embed = discord.Embed(title = f"이 명령어를 {ctx.author} 의 권한 부족으로 실행하지 못했습니다.", description = "관리자에게 권한 추가를 요청해 보세요.", color = 0xff0000)
        await ctx.send(embed=embed)
    
    if error_notfound == True:
        embed = discord.Embed(title="Error Info", description="Koi_Bot Error Info", color=0xff0000)
    embed.add_field(name="Error Info", value=f"```{error}```")
    await ctx.send(embed=embed)

cnt = 0

@app.event
async def on_message(message):
    if message.author.bot:
        if str(message.author) != "KOI_TEST#8688": #Calling from Koi_Bot_Client
            return None
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%H:%M:%S')
    print(str(nowDatetime) + " - " + str(message.author) + " : " + str(message.content))
    await app.process_commands(message)
    if message.content[:2] == "//":
        await message.channel.send("Now updating Koi_Bot. Be aware of data.")
    if message.content[:4] == "코이야 ":
        if str(message.author) == "KOI_TEST#8688": #Calling from Koi_Bot_Client
            await message.channel.send("호출어0 " + str(kogpt2.Chat_To_AI(message.content[4:])))
        else:
            await message.channel.send(str(kogpt2.Chat_To_AI(message.content[4:])))
    

app.run(get_token())