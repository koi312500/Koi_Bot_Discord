import sqlite3
import discord
from discord.ext import commands

from Config import Config

sql_db = sqlite3.connect("Data/User_DB/test.db")
db_cursor = sql_db.cursor()
class SQLTest(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "sql_test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def sql_test_command(self, ctx, user_name : discord.Member, money):
        if ctx.author.id not in Config.admin_id:
            embed = discord.Embed(title = f"이 명령어는 관리자용/개발중인 명령어이며, Developer만 사용하실 수 있습니다.", color = 0xff0000)
            await ctx.reply(embed = embed, mention_author = False)
            return

        await ctx.channel.send("Passed! - test1")
        db_cursor.execute("INSERT INTO USER_INFO VALUES(?,?);", (user_name.id,money))
        await ctx.channel.send("Passed! - test2")
        sql_db.commit()
def setup(app):
    app.add_cog(SQLTest(app))