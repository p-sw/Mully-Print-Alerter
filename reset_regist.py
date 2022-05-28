import psycopg2 as pg
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT

db = pg.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    port=DB_PORT
)

cursor = db.cursor()
cursor.execute('DELETE FROM regist_info')
db.commit()
print('JOB DONE.')