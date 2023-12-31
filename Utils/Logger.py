from datetime import datetime
import os

# Function to handle errors
def err(error):
    log(f'[Error] {error}', True)
    return error

# Async function to send information to specific channels
async def info(msg: str, app):
    channel = app.get_channel(865999145600286741)  # Channel ID for logging
    channel2 = app.get_channel(1110799032000978974)  # Another Channel ID for logging
    text = f'[Info] {msg}'
    await channel.send(f'Koi_Bot Logging - {text}')  # Sending info to first channel
    await channel2.send(f'Koi_Bot Logging - {text}')  # Sending info to second channel
    log(text)

# Function to handle logging messages
def msg(message):
    if message.content == "":
        return

    author = message.author

    if 'DM' in str(type(message.channel)):
        log_msg = f"[Message/DM] <{str(author)}> {message.content}"  # Logging DM messages
    else:
        guild = message.guild
        channel = message.channel
        log_msg = f"[Message/Server] <{guild.name} | {channel.name} | {str(author)} | {author.id}> {message.content}"  # Logging server messages

    log(log_msg)

# Function to log messages and optionally errors
def log(msg: str, iserror=False):
    now = datetime.now()
    nowDatetime = now.strftime('%H:%M:%S')
    log_msg = f"{nowDatetime}ㆍ{msg}"
    print(log_msg)  # Printing log message to console
    save(log_msg)  # Saving log message to a text file
    if iserror:
        save_error(log_msg)  # Saving error message to a separate text file if 'iserror' is True

# Function to save logs to a text file
def save(msg):
    now = datetime.now()
    time_text = now.strftime('%Y-%m-%d')
    if not os.path.isfile("Data/Logs/log_" + time_text + ".txt"):
        f = open("Data/Logs/log_" + time_text + ".txt", 'w', encoding='utf-8')
    else:
        f = open("Data/Logs/log_" + time_text + ".txt", 'a', encoding='utf-8')
    f.write(msg + '\n')
    f.close()

# Function to save error logs to a separate text file
def save_error(msg):
    now = datetime.now()
    time_text = now.strftime('%Y-%m-%d')
    if not os.path.isfile("Data/Logs/error_log_" + time_text + ".txt"):
        f = open("Data/Logs/error_log_" + time_text + ".txt", 'w', encoding='utf-8')
    else:
        f = open("Data/Logs/error_log_" + time_text + ".txt", 'a', encoding='utf-8')
    f.write(msg + '\n')
    f.close()
