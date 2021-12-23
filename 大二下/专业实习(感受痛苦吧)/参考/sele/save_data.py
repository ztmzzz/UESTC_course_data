import pymysql


class ToSql(object):
    def __init__(self):
        self.host = ""
        self.user = ""
        self.pw = ""
        self.db = ""
        self.conn = pymysql.Connect(host=self.host, user=self.user, password=self.pw, database=self.db)
        self.cursor = self.conn.cursor()
        self.insert_sql = """
            INSERT INTO major_line_2018(school_name, province, exam_type, year, max_score, average, min_score, batch, 
            major_name, search_word) VALUES(%s);
        """ % ('"%s",'*9 + '"%s"')

    def insert(self, data):
        try:
            self.cursor.execute(self.insert_sql % data)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e, data)

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    obj = ToSql()
    obj.close()


