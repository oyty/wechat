# coding=utf-8
__author__ = 'oyty'

import MySQLdb as mdb

con = None

try:
    con = mdb.connect(host='localhost', user='root', passwd='892968', db='oyty', charset='utf8')

    cur = con.cursor()
    content = '明月'
    cur.execute("SELECT * FROM poem WHERE poem LIKE '%" + content + "%'")
    poems = cur.fetchall()
    print poems[0][1]




finally:
    if con:
        con.close()
