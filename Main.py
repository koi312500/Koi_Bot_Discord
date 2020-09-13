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

@commands.has_permissions(administrator = True)
@app.command(name = "test", pass_context = True)
async def Test(ctx, num1 = None):
    await ctx.send("Test succeed")

@commands.has_permissions(kick_members = True)
@app.command(name = "kick", pass_context = True)
async def _kick(ctx, user_name : discord.Member, *, reason = None):
    print(reason)
    await user_name.kick(reason = reason)
    if(reason != None):
        await ctx.send(str(user_name) + "님이 추방되셨습니다." + "\n이유 : " + str(reason))
    else:
        await ctx.send(str(user_name) + "님이 추방되셨습니다.")

@commands.has_permissions(ban_members = True)
@app.command(name = "ban", pass_context = True)
async def _ban(ctx, user_name : discord.Member, *, reason = None):
    await user_name.ban(reason = reason)
    if(reason != None):
        await ctx.send(str(user_name) + "님이 차단되셨습니다." + "\n이유 : " + str(reason))
    else:
        await ctx.send(str(user_name) + "님이 차단되셨습니다.")

@commands.has_permissions(ban_members = True)
@app.command(name = "unban", pass_context = True)
async def _unban(ctx, *, user_name):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = user_name.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} 의 차단이 해제되셨습니다.")
            return

@commands.has_permissions(manage_messages=True)
@app.command(name = "delete", pass_context = True)
async def _clean(ctx, amount):
    await ctx.channel.purge(limit = int(amount))
    await ctx.send(str(amount) + "개의 메세지를 지웠습니다.")


@app.command(name = "Dement", pass_context = True) #Test command
async def _Dement(ctx):
    for i in range(0,3000):
        my_name = discord.utils.get(ctx.guild.members, name="요잇")
        await ctx.channel.send("{}".format(my_name.mention))

@app.command(name = "compile", pass_context = True) #Compile code in many language - v1
async def _compile(ctx, *, command):
    lines = command.splitlines()
    language = lines[0][3:]
    language.lower()
    
    print(language)
    if language == "java":
        print("Test succeedd")
    size = len(lines)
    text = open("temp." + language, "w+")
    for i in range(1, size):
        if(i == size-1):
            if lines[i] == "```":
                break
            else:
                text.write(lines[i][:3])
                break
        text.write(lines[i] + "\n")
    print("done")
        

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