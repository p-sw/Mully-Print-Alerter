import os
from urllib.parse import urlparse

target_url = "http://bupyeong.icehs.kr/boardCnts/list.do?boardID=290173&m=0903&s=bupyeong"
guild_id=["939031979893088328", "979944212051148813"]

DB_URI = os.environ.get('DB_URI')
PARSED_URI = urlparse(DB_URI)
DB_HOST = PARSED_URI.hostname
DB_NAME = PARSED_URI.path[1:]
DB_USER = PARSED_URI.username
DB_PASS = PARSED_URI.password
DB_PORT = PARSED_URI.port