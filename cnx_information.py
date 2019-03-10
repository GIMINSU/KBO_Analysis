from config import config
import pymysql

class BaseManager:
    def get_cnx(self, db_name, **kwargs):
        db = config['db'][db_name]
        engine = db['engine']

        if engine == "MySQL":
            cnx = pymysql.connect(user=db['user'], password=db['password'],
                                  host=db['host'], database=db['database'],
                                  charset='utf8mb4', **kwargs
                                  )
            return cnx