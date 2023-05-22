from discord.ext import commands
from discord.ext import tasks
from discord.commands import slash_command

import psutil
import socket

from config import Slash_Command_Server as SCS
from Utils import Permission
from Utils import Logger

class LapTopManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.battery_status_check.start()

    @tasks.loop(minutes = 5)
    async def battery_status_check(self):
        battery = psutil.sensors_battery()
        if battery.power_plugged is not True:
            channel = await self.bot.fetch_channel(865999145600286741)
            await channel.send(f"Laptop's battery status : {battery.percent}%, Power : {battery.power_plugged}")
            await channel.send(f"Warning!!! Warning Message to : <@753625063357546556>\nBattery is unplugged, please shutdown the computer or solve the problem please.")
        
    @slash_command(name = "battery_info", guild_ids = SCS)
    async def battery_info_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None

        battery = psutil.sensors_battery()
        await ctx.respond(f"Laptop's battery status : {battery.percent}%, Power : {battery.power_plugged}")

    @slash_command(name = "ip_info", guild_ids = SCS)
    async def ip_info_command(self, ctx):
        if await Permission.check_permission(ctx, 3):
            return None

        hostname = socket.gethostname()
        IpAddr = socket.gethostbyname(hostname)
        await ctx.respond(f"Computer's name : {hostname}\nComputer's IP : {IpAddr}")
                        

def setup(bot):
    bot.add_cog(LapTopManagement(bot))
