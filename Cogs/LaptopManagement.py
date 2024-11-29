from discord.ext import commands
from discord.ext import tasks
from discord.commands import slash_command

import asyncio
import socket
import requests

# Importing configuration and utilities
import config
from config import Slash_Command_Server as SCS
from Utils import Permission
from Utils import Logger

class LapTopManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # Starting a background task to check laptop's battery status
        self.battery_status_check.start()

    # Task to check laptop's battery status every 15 minutes
    @tasks.loop(minutes=15)
    async def battery_status_check(self):
        battery = open("/sys/class/power_supply/CMB0/capacity","r").readline().strip()
        if int(battery) < 50:
            # Fetching a specific channel and sending battery status and alerts
            battery = open("/sys/class/power_supply/CMB0/capacity","r").readline().strip()
            charge_state=open("/sys/class/power_supply/CMB0/status","r").readline().strip()
            channel = await self.bot.fetch_channel(865999145600286741)
            await channel.send(f"Laptop's battery status : {battery}%, Power : {charge_state}")
            await channel.send(f"서버의 충전상태를 확인해주시기 바랍니다.\nAlert : <@753625063357546556>.")
        
    # Slash command to get laptop's battery information
    @slash_command(name="battery_info", guild_ids=SCS)
    async def battery_info_command(self, ctx):
        if await Permission.check_permission(ctx, 2):
            return None

        battery = open("/sys/class/power_supply/CMB0/capacity","r").readline().strip()
        charge_state=open("/sys/class/power_supply/CMB0/status","r").readline().strip()
        await ctx.respond(f"Laptop's battery percentage : {battery}%, Power : {charge_state}")

    # Slash command to get computer's name and IP address
    @slash_command(name="ip_info", guild_ids=SCS)
    async def ip_info_command(self, ctx):
        if await Permission.check_permission(ctx, 2):
            return None

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        ip = requests.get("https://api.ipify.org").text
        await ctx.respond(f"Computer's Private IP: {s.getsockname()[0]}\nComputer's Public IP : {ip}")
                        
# Function to setup the cog
def setup(bot):
    bot.add_cog(LapTopManagement(bot))
