import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, app):
        self.app = app

    @cog_ext.cog_slash(name="SlashTest")
    async def SlashTest(self, ctx: SlashContext):
        embed = discord.Embed(title="embed test")
        await ctx.send(content="test", embeds=[embed])

def setup(app):
    app.add_cog(Slash(app))