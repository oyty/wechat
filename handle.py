# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import reply
import MySQLdb as mdb
import sys

class Handle(object):
    def POST(self):
        con = None
        try:
            reload(sys)
            sys.setdefaultencoding('utf-8')
            webData = web.data()
            print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            con = mdb.connect(host='localhost', user='root', passwd='892968', db='oyty', charset='utf8')
            cur = con.cursor()
            cur.execute("SELECT * FROM poem WHERE poem LIKE '%" + recMsg.Content + "%'")
            poems = cur.fetchall()
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                print poems[0][1]
                content = poems[0][1]
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                content = poems[0][1]
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            if con:
                con.close()
            return Argment

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "oyty520214"  # 请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
