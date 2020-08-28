import asyncio
import discord
app = discord.Client()

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



@app.event
async def on_message(message):
    if message.author.bot:
        return None
    

get_token()
app.run(token)