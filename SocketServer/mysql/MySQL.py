import pymysql

class MySQL:
    def __init__(self, mysql_config):
        self.user = mysql_config["user"]
        self.password = mysql_config["password"]
        self.host = mysql_config["host"]
        self.db = mysql_config["db"]
        self.charset = mysql_config["charset"]

    def connect(self):
        try:
            self.mysql = pymysql.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                db = self.db,
                charset = self.charset
            )
            print("mysql connect!")
        except Exception as e:
            print(e)

    def query(self, sql):
        with self.mysql.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        self.mysql.commit()
        return rows