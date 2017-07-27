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

            if len(recMsg.Content) < 2:
                content = u"请输入至少两位关键词"
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()

            con = mdb.connect(host='localhost', user='root', passwd='892968', db='oyty', charset='utf8')
            cur = con.cursor()
            cur.execute("SELECT * FROM poem WHERE poem LIKE '%" + recMsg.Content + "%' LIMIT 1, 11")
            poems = cur.fetchall()
            content = ''
            if len(poems) == 0:
                content = u"未查询到相关诗文，请重新输入"
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()

            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                for i in range(0, 10):
                    poetry = poems[i][1] + "\n" + '<a href="' + poems[i][3] + '">' + poems[i][2] + "</a>\n\n"
                    content = content + poetry
                if len(poems) > 10:
                    content += "最多匹配10条，可修改关键字，提高查询精度"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            if isinstance(recMsg, receive.EventMsg):
                if recMsg.Event == 'CLICK':
                    if recMsg.Eventkey == 'queryRule':
                        content = u"欢迎使用~\n1关键词  搜索诗词\n2诗人名  搜索诗人的诗词".encode('utf-8')
                        toUser = recMsg.FromUserName
                        fromUser = recMsg.ToUserName
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
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
