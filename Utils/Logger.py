#Originated from Kimu-Nowchira's Setabot Framework
#Edited by KOI#4182

from datetime import datetime
import os

def err(error):
    log(f'[Error] {error}', True)
    return error

async def info(msg: str, app):
    channel = app.get_channel(865999145600286741)
    text = f'[Info] {msg}'
    await channel.send(f'Koi_Bot Logging - {text}')
    log(text)

def msg(message):
    if message.content == "":
        return

    author = message.author

    if 'DM' in str(type(message.channel)):
        log_msg = f"[Message/DM] <{str(author)}> {message.content}"
    else:
        guild = message.guild
        channel = message.channel
        log_msg = f"[Message/Server] <{guild.name} | {channel.name} | {str(author)} | {author.id}> {message.content}"

    log(log_msg)


def log(msg: str, iserror=False):
    now = datetime.now()
    nowDatetime = now.strftime('%H:%M:%S')
    log_msg = f"{nowDatetime}ㆍ{msg}"
    print(log_msg)
    save(log_msg)
    if iserror:
        save_error(log_msg)


def save(msg):
    now = datetime.now()
    time_text = now.strftime('%Y-%m-%d')
    if not os.path.isfile("Data/Logs/log_" + time_text + ".txt"):
        f = open("Data/Logs/log_" + time_text + ".txt", 'w', encoding='utf-8')
    else:
        f = open("Data/Logs/log_" + time_text + ".txt", 'a', encoding='utf-8')
    f.write(msg + '\n')
    f.close()


def save_error(msg):
    now = datetime.now()
    time_text = now.strftime('%Y-%m-%d')
    if not os.path.isfile("Data/Logs/error_log_" + time_text + ".txt"):
        f = open("Data/Logs/error_log_" + time_text + ".txt", 'w', encoding='utf-8')
    else:
        f = open("Data/Logs/error_log_" + time_text + ".txt", 'a', encoding='utf-8')
    f.write(msg + '\n')
    f.close()