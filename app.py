__author__ = 'oyty'

import web
from handle import Handle
import MySQLdb as mdb

con = None

try:
    con = mdb.connect('localhost', 'root', '892968', 'oyty')
finally:
    if con:
        con.close()

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
