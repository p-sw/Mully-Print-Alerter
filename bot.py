import os
import discord
from discord.ext import tasks
import requests
from bs4 import BeautifulSoup

bot = discord.Bot()

#* Initial Setting *#
alert_guild = 0
alert_channel = 0

target_url = "http://bupyeong.icehs.kr/boardCnts/list.do?boardID=290173&m=0903&s=bupyeong"

#*******************#

@bot.event
async def on_ready():
    print(f"Ready for {bot.user}")

@bot.slash_command()
async def set_channel(ctx):
    global alert_guild, alert_channel
    print(f"Setting channel to {ctx.guild.id}:{ctx.channel.id}")
    alert_guild = ctx.guild.id
    alert_channel = ctx.channel.id
    print(f"Set channel to {alert_guild}:{alert_channel}")


async def get_news():
    response = requests.get(target_url)
    print(response.content)


@tasks.loop(hours=2)
async def check_news():
    await get_news()



bot.run(os.environ.get("token"))