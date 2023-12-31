import discord
from discord.ext import commands
from discord.commands import slash_command

import asyncio

from Utils import Permission

class ServerManagement(commands.Cog):

    def __init__(self, app):
        self.app = app
    
    # Command to kick a member
    @commands.has_permissions(kick_members=True)
    @slash_command(name="kick")
    async def kick_command(self, ctx, user_name: discord.Member, *, reason=None):
        if await Permission.check_permission(ctx, 1):
            return None
        await user_name.kick(reason=reason)
        if reason is not None:
            await ctx.respond(f"{user_name}님이 추방되셨습니다.\n이유 : {reason}")
        else:
            await ctx.respond(f"{user_name}님이 추방되셨습니다.")

    # Command to ban a member
    @commands.has_permissions(ban_members=True)
    @slash_command(name="ban")
    async def ban_command(self, ctx, user_name: discord.Member, *, reason=None):
        if await Permission.check_permission(ctx, 1):
            return None
        await user_name.ban(reason=reason)
        if reason is not None:
            await ctx.respond(f"{user_name}님이 차단되셨습니다.\n이유 : {reason}")
        else:
            await ctx.respond(f"{user_name}님이 차단되셨습니다.")

    # Command to unban a previously banned member
    @commands.has_permissions(ban_members=True)
    @slash_command(name="unban")
    async def unban_command(self, ctx, *, user_name):
        if await Permission.check_permission(ctx, 1):
            return None
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = user_name.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.respond(f"{user.mention}의 차단이 해제되셨습니다.")
                return

    # Command to delete a specified number of messages in a channel
    @commands.has_permissions(manage_messages=True)
    @slash_command(name="delete")
    async def delete_command(self, ctx, amount):
        if await Permission.check_permission(ctx, 1):
            return None
        await ctx.channel.purge(limit=int(amount))
        message = await ctx.respond(f"{amount}개의 메세지를 지웠습니다.")
        await asyncio.sleep(3)
        await message.delete_original_response()

# Function to setup the cog
def setup(app):
    app.add_cog(ServerManagement(app))
