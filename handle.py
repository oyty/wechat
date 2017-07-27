# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import reply


class Handle(object):
    def POST(self):
        webData = web.data()
        print "Handle Post webdata is \n", webData  # 后台打日志
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = "test"
            print content
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            print receive.parse_xml(replyMsg)
            return replyMsg.send()
        else:
            print "暂且不处理"
            return "success"

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
