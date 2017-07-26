# encoding=utf-8
__author__ = 'oyty'

import urllib2
from bs4 import BeautifulSoup
import MySQLdb as mdb

base_url = 'http://so.gushiwen.org/mingju/Default.aspx?p='
base_home_url = 'http://so.gushiwen.org'

count_size = 1


def parse_data(url, count_size=None):
    request = urllib2.Request(url)
    html = urllib2.urlopen(request)

    soup = BeautifulSoup(html, 'lxml')
    div_all = soup.find('div', {'class': 'sons'})
    divs = div_all.find_all('div')

    print '第' + str(count_size) + '页数据\n'
    print 'there are ' + str(len(divs)) + ' data'

    con = mdb.connect('localhost', 'root', '892968', 'oyty')
    con.set_character_set('utf8')
    cur = con.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS poem(id INT PRIMARY KEY AUTO_INCREMENT, poem VARCHAR(80), author VARCHAR(40), href VARCHAR(100))')

    for i in range(0, len(divs)):
        lines = divs[i].findAll('a')
        poem = lines[0].text.strip()
        author = lines[1].text.strip()
        href = base_home_url + lines[0]['href']
        # poem = poem.decode("gbk").encode("utf-8")
        # author = author.decode("gbk").encode("utf-8")
        # href = href.decode("gbk").encode("utf-8")
        cur.execute("INSERT INTO poem(poem, author, href) VALUES('" + poem + "','" + author + "','" + href + "'" + ")")
        con.commit()
        print poem + '\n'
    count_size += 1
    if count_size == 5668:
        return
    parse_data(base_url + str(count_size) + '&c=&t=', count_size)


if __name__ == "__main__":
    url = base_url + str(count_size) + '&c=&t='
    parse_data(url, 1)
