__author__ = 'oyty'

import MySQLdb as mdb

con = None

try:
    con = mdb.connect('localhost', 'root', '892968', 'oyty')

    cur = con.cursor()



finally:
    if con:
        con.close()
