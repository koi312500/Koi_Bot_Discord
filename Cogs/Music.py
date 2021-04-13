import discord
from discord.ext import commands

class Music(commands.Cog):

    def __init__(self, app):
        self.app = app
    
    @commands.command(name = "join")
    async def music_join_command(self, ctx):
        voice_channel_id = ctx.author.voice.channel.id
        voice_channel = ctx.guild.get_channel(voice_channel_id)
        await voice_channel.connect()
    
    @commands.command(name = "leave")
    async def music_leave_command(self, ctx):
        voice_channel_id = ctx.author.voice.channel.id
        voice_channel = ctx.guild.get_channel(voice_channel_id)
        await voice_channel.disconnect()

def setup(app):
    app.add_cog(Music(commands))