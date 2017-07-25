# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import reply

class Handle(object):
    def POST(self):
        try:
            web_data = web.data()
            print 'Handle post web data is ', web_data
            rec_msg = receive.parse_xml(web_data)
            if isinstance(rec_msg, receive.Msg) and rec_msg.msg_type == 'text':
                toUser = rec_msg.FromUserName
                fromUser = rec_msg.ToUserName
                content = "test"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"

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
            token = "oyty520214" #请按照公众平台官网\基本配置中信息填写

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