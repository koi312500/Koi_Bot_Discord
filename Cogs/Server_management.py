import discord
from discord.ext import commands

class ServerManagement(commands.Cog):

    def __init__(self, app):
        self.app = app
    
    @commands.has_permissions(kick_members = True)
    @commands.command(name = "kick", help = "멤버를 추방합니다.")
    async def kick_command(self, ctx, user_name : discord.Member, *, reason = None):
        await user_name.kick(reason = reason)
        if(reason != None):
            await ctx.send(str(user_name) + "님이 추방되셨습니다." + "\n이유 : " + str(reason))
        else:
            await ctx.send(str(user_name) + "님이 추방되셨습니다.")

    @commands.has_permissions(ban_members = True)
    @commands.command(name = "ban")
    async def ban_command(self, ctx, user_name : discord.Member, *, reason = None):
        await user_name.ban(reason = reason)
        if(reason != None):
            await ctx.send(str(user_name) + "님이 차단되셨습니다." + "\n이유 : " + str(reason))
        else:
            await ctx.send(str(user_name) + "님이 차단되셨습니다.")

    @commands.has_permissions(ban_members = True)
    @commands.command(name = "unban")
    async def unban_command(self, ctx, *, user_name):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = user_name.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} 의 차단이 해제되셨습니다.")
                return

    @commands.has_permissions(manage_messages=True)
    @commands.command(name = "delete")
    async def delete_command(self, ctx, amount):
        await ctx.channel.purge(limit = int(amount))
        await ctx.send(str(amount) + "개의 메세지를 지웠습니다.")


def setup(app):
    app.add_cog(ServerManagement(commands))