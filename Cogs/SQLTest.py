import sqlite3
import discord
from discord.ext import commands
sql_db = sqlite3.connect("./User_data/test.db")
db_cursor = sql_db.cursor()

class SQLTest(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command(name = "sql_test", help = "관리자용 커맨드입니다.", usage = "관리자용 커맨드입니다.")
    async def sql_test_command(self, ctx, user_name : discord.Member, money):
        await ctx.channel.send("Passed! - test1")
        db_cursor.execute("INSERT INTO USER_INFO VALUES(?,?);", (user_name.id,money))
        await ctx.channel.send("Passed! - test2")
        sql_db.commit()
def setup(app):
    app.add_cog(SQLTest(app))