# -*- coding: UTF-8 -*-
import MySQLdb


class SQL:
    def __init__(self, database):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", database, charset="utf8")

    def select(self, Sqlstr):
        cur = self.db.cursor()
        cur.execute(Sqlstr)
        return cur.fetchall()

    def IDU(self, Sqlstr):
        cur = self.db.cursor()
        cur.execute(Sqlstr)
        self.db.commit()

    def close(self):
        self.db.close()
