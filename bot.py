import os
import discord
from discord.ext import tasks
from discord.embeds import Embed
from utils import DB, get_news, factor_to_link, get_files
from settings import guild_id

bot = discord.Bot()
db = DB()

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
    INSERT INTO regist_info VALUES ('{ctx.channel.id}')
    '''
    await db.execute(sql)
    print(f"Set channel to {ctx.channel.id}")
    await ctx.respond('Channel set.')


async def alert_news(news):
    channel_ids = await db.execute_get('SELECT * FROM regist_info')
    channels = [await bot.fetch_channel(int(cn_id[0])) for cn_id in channel_ids]

    for channel in channels:
        for dt in news:
            embed = Embed(title="새로운 물리 자료", description=dt[0])
            link_value = f"[게시글 바로가기]({await factor_to_link(dt[1])})"
            attaches = await get_files(dt[1])
            attaches_value = '\n'.join([f"[파일: {attach[0]}](http://bupyeong.icehs.kr/{attach[1]})" for attach in attaches])
            print(attaches_value)
            embed.add_field(name='링크', value=link_value, inline=False)
            embed.add_field(name='첨부파일 다운로드', value=attaches_value, inline=False)
            await channel.send(content="@everyone", embed=embed)
        

@tasks.loop(hours=2)
async def check_news():
    print("Checking news in board..")
    db_sql = 'SELECT * FROM board_history'
    fresh_data = await get_news()
    db_data = await db.execute_get(db_sql)
    if fresh_data != db_data:
        print("Updating..")
        sql_insert = ""
        freshes = []
        for dt in fresh_data:
            sql_query_exists = f'SELECT * FROM board_history WHERE factor="{dt[1]}"'
            db_result = await db.execute_get(sql_query_exists)
            if not db_result:
                sql_insert += f'INSERT INTO board_history VALUES ("{dt[0]}", "{dt[1]}");'
                print(f"New value found ({dt[0]}, {dt[1]})")
                freshes.append(dt)
            else:
                print(f"Existing values ({dt[0]}, {dt[1]})")
        await alert_news(freshes)
        await db.execute(sql_insert)
    print("Done!")


bot.run(os.environ.get("token"))