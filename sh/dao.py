#*-coding:utf-8-*-
import pymysql

class DAO:
    def __init__(self):
        self.HOST = 'hantestdb.cklwl7rg6i5n.ap-northeast-2.rds.amazonaws.com'
        self.conn = pymysql.connect(host=self.HOST, user='HANJH', password='gksdldma#VIC', db='testdb')
        self.curs = self.conn.cursor()


    def insert_data(self,id,content):
        sql = """insert into dialogue values ('%s', '%s', now())"""%(id,content)
        #sql = """insert into user_info  values ('현few', '인냥', now())"""
        self.conn.query("set character_set_connection=utf8;")
        self.conn.query("set character_set_server=utf8;")
        self.conn.query("set character_set_client=utf8;")
        self.conn.query("set character_set_results=utf8;")
        self.conn.query("set character_set_database=utf8;")
        #self.curs.execute(sql.encode('utf8'))
        self.curs.execute(sql.encode('utf8'))
        self.conn.commit()





#a = DAO()
#a.insert_data("수현","ㅅㄷㅅㄷㅈㅅㅈㄷ")


