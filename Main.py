import asyncio
import discord
from discord.ext import commands
import sys
sys.path.insert(1, 'KoGPT2-chatbot')
import AI_talk as kogpt2

app = commands.Bot(command_prefix = "//")

def get_token():
    global token
    f = open("Key.key", "r")
    token = str(f.readline())

@app.event
async def on_ready():
    print("다음으로 로그인합니다 : ")
    print(app.user.name)
    print(app.user.id)
    print("==========")
    game = discord.Game("Koi Bot이 정상 실행 중입니다!")
    await app.change_presence(status=discord.Status.online, activity=game)
    kogpt2.Load_Model()

@app.event
async def on_message(message):
    await app.process_commands(message)
    if message.author.bot:
        return None
    if message.content[:4] == "코이야 ":
        await message.channel.send(kogpt2.Chat_To_AI(message.content[4:]))
        print(message.content)
    

get_token()
app.run(token)