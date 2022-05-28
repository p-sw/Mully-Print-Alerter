import os
from urllib.parse import urlparse

target_url = "http://bupyeong.icehs.kr/boardCnts/list.do?boardID=290173&m=0903&s=bupyeong"
guild_id=["939031979893088328", "979944212051148813"]

DB_URL = os.environ.get('DATABASE_URL')
PARSED_URL = urlparse(DB_URL)
DB_HOST = PARSED_URL.hostname
DB_NAME = PARSED_URL.path[1:]
DB_USER = PARSED_URL.username
DB_PASS = PARSED_URL.password
DB_PORT = PARSED_URL.port