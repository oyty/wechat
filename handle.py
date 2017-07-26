# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import reply

import MySQLdb as mdb

class Handle(object):
    def __init__(self):
        pass

    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is \n", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            print '\n rece_msg----', recMsg.Content
            con = None
            try:
                con = mdb.connect(host='localhost', user='root', passwd='892968', db='oyty', charset='utf8')
                cur = con.cursor()
                cur.execute("SELECT * FROM poem WHERE poem LIKE '%" + recMsg.Content + "%'")
                poems = cur.fetchall()
                print poems[0][1]
                if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                    toUser = recMsg.FromUserName
                    fromUser = recMsg.ToUserName
                    content = poems[0][1]
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                else:
                    print "暂且不处理"
                    return "success"
            finally:
                if con:
                    con.close()


        except Exception, Argment:
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
