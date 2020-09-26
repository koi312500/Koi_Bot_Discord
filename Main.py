import asyncio
import discord
import os
from discord.ext import commands
import sys
sys.path.insert(1, 'KoGPT2-chatbot')
import AI_talk as kogpt2

app = commands.Bot(command_prefix = "//")
app.remove_command("help")

def get_token(): # Get tokens from key.key
    with open("Key.key", "r") as f:
        return f.readline().strip()

@app.event # Statement changing
async def on_ready():
    print("Logining to : " + str(app.user.name) + "(code : " + str(app.user.id) + ")")
    game = discord.Game("Now updating Koi Bot")
    await app.change_presence(status=discord.Status.idle, activity=game)

for filename in os.listdir("Cogs"): # Get all Cogs from Cogs folder
    if filename.endswith(".py"):
        app.load_extension(f"Cogs.{filename[:-3]}")

@app.command(name="load")
async def load_commands(ctx, extension):
    app.load_extension(f"Cogs.{extension}")
    await ctx.send(f"{extension} is loaded successfully!")

@app.command(name="unload")
async def unload_commands(ctx, extension):
    app.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"{extension} is unloaded successfully!")

@app.command(name="reload")
async def reload_commands(ctx, extension=None):
    if extension is None:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                app.unload_extension(f"Cogs.{filename[:-3]}")
                app.load_extension(f"Cogs.{filename[:-3]}")
        await ctx.send("All extension is reloaded successfully!")
    else:
        app.unload_extension(f"Cogs.{extension}")
        app.load_extension(f"Cogs.{extension}")
        await ctx.send(f"{extension} is reloaded successfully!")

@app.command(name = "help") # Help command
async def help_command(ctx,func = None):
    cog_list = ["ServerManagement", "Compile", "Development"]
    if func is None:
        embed = discord.Embed(title="Koi_Bot 도움말", description="명령 구문은 //`명령어` 입니다.", color=0x00ffff) 
        embed.set_footer(text="//help `명령어`로 특정 명령어의 자세한 설명을 보실 수 있습니다!")
        for x in cog_list:
            cog_data = app.get_cog(x)
            command_list = cog_data.get_commands()
            embed.add_field(name=x, value=" ".join([c.name for c in command_list]), inline=True) 
        await ctx.send(embed=embed)
    else: # func가 None이 아니면
        command_notfound = True # 이걸 어떻게 쓸지 생각해보세요!
        for _title, cog in app.cogs.items(): # title, cog로 item을 돌려주는데 title은 필요가 없습니다.
            if not command_notfound: # False면
                break # 반복문 나가기

            else: # 아니면
                for title in cog.get_commands(): # 명령어를 아까처럼 구하고 title에 순차적으로 넣습니다.
                    if title.name == func: # title.name이 func와 같으면
                        cmd = app.get_command(title.name) # title의 명령어 데이터를 구합니다.
                        embed = discord.Embed(title=f"명령어 : {cmd}", description=cmd.help, color=0x00ffff) # Embed 만들기
                        embed.set_footer(text="//help `명령어`로 특정 명령어의 자세한 설명을 보실 수 있습니다!")
                        embed.add_field(name="사용법", value=cmd.usage) # 사용법 추가
                        await ctx.send(embed=embed) # 보내기
                        command_notfound = False
                        break # 반복문 나가기
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
async def on_message(message):
    await app.process_commands(message)
    if message.author.bot:
        return None
    if message.content[:2] == "//":
        await message.channel.send("Now updating Koi_Bot. Be aware of data.")
    if message.content[:4] == "코이야 ":
        await message.channel.send(kogpt2.Chat_To_AI(message.content[4:]))
        print(message.content)
    

app.run(get_token())