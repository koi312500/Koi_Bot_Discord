import discord
from discord.ext import commands

from Utils import Permission
class ServerManagement(commands.Cog):

    def __init__(self, app):
        self.app = app
    
    @commands.has_permissions(kick_members = True)
    @commands.command(name = "kick", help = "멤버를 추방합니다.", usage = "//kick 대상(멘션)\nEx : //kick @AKMU_LOVE#4211")
    async def kick_command(self, ctx, user_name : discord.Member, *, reason = None):
        if await Permission.check_permission(ctx, 1):
            return None
        await user_name.kick(reason = reason)
        if(reason != None):
            await ctx.reply(str(user_name) + "님이 추방되셨습니다." + "\n이유 : " + str(reason), mention_author = False)
        else:
            await ctx.reply(str(user_name) + "님이 추방되셨습니다.", mention_author = False)

    @commands.has_permissions(ban_members = True)
    @commands.command(name = "ban", help = "멤버를 차단합니다.", usage = "//ban 대상(멘션)\nEx : //ban @AKMU_LOVE#4211")
    async def ban_command(self, ctx, user_name : discord.Member, *, reason = None):
        if await Permission.check_permission(ctx, 1):
            return None
        await user_name.ban(reason = reason)
        if(reason != None):
            await ctx.reply(str(user_name) + "님이 차단되셨습니다." + "\n이유 : " + str(reason), mention_author = False)
        else:
            await ctx.reply(str(user_name) + "님이 차단되셨습니다.", mention_author = False)

    @commands.has_permissions(ban_members = True)
    @commands.command(name = "unban", help = "멤버의 차단을 해제합니다.", usage = "//unban 대상(멘션 X)\nEx : //unban AKMU_LOVE#4211")
    async def unban_command(self, ctx, *, user_name):
        if await Permission.check_permission(ctx, 1):
            return None
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = user_name.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.reply(f"{user.mention} 의 차단이 해제되셨습니다.", mention_author = False)
                return

    @commands.has_permissions(manage_messages=True)
    @commands.command(name = "delete", help = "메세지를 삭제합니다.", usage = "//delete 삭제하고 싶은 메세지 개수\nEx : //delete 100")
    async def delete_command(self, ctx, amount):
        if await Permission.check_permission(ctx, 1):
            return None
        await ctx.channel.purge(limit = int(amount))
        await ctx.send(str(amount) + "개의 메세지를 지웠습니다.")


def setup(app):
    app.add_cog(ServerManagement(app))