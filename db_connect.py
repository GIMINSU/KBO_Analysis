import config
import pymysql
from pymysql.cursors import DictCursor

def db_connect():
    conn = pymysql.connect(
        database=config['db']['local']['name'],
        host=config['db']['local']['host'],
        user=config['db']['local']['user'],
        password=config['db']['local']['password'],
        charset='utf8mb4',
        autocommit=False,
        cursorclass=DictCursor,
    )
    return conn