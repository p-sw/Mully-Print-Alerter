import os
import discord
from discord.ext import tasks
from utils import DB, get_news
from settings import guild_id

bot = discord.Bot()
db = DB("db.db")

@bot.event
async def on_ready():
    print(f"Ready for {bot.user}")
    print("Preparing db..")
    initial_sql = '''
    CREATE TABLE IF NOT EXISTS regist_info (channel_id string);
    CREATE TABLE IF NOT EXISTS board_history (title string, factor string);
    '''
    await db.execute(initial_sql)
    print("Preparing tasks..")
    check_news.start()

@bot.slash_command(guild_ids=guild_id)
async def set_channel(ctx):
    print(f"Setting channel to {ctx.channel.id}")
    sql = f'''
    INSERT INTO regist_info VALUSE ('{ctx.channel.id}')
    '''
    await db.execute(sql)
    print(f"Set channel to {ctx.channel.id}")


@tasks.loop(hours=2)
async def check_news():
    print("Checking news in board..")
    db_sql = '''
    SELECT * FROM board_history
    '''
    fresh_data = await get_news()
    db_data = await db.execute_get(db_sql)
    print(fresh_data)
    print(db_data)
    if fresh_data != db_data:
        print("Updating..")
        sql = '''
        DELETE FROM board_history;
        '''
        for dt in fresh_data:
            sql += f'INSERT INTO board_history VALUES ("{dt[0]}", "{dt[1]}");'
        await db.execute(sql)
    print("Done!")


bot.run(os.environ.get("token"))