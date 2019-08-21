#!/usr/bin/python
#encoding=utf8
import dns.resolver
import os
import httplib
iplist = []
appdomain = "www.baidu.com"
def get_iplist(domain=""):# 域名函数，解析ip追加到iplist
    try:
        A = dns.resolver.query(domain, 'A') # 解析A记录
    except Exception,e:#错误输出
        print "dns reslover error:" + str(e)
        return
    for i in A.response.answer:
        for j in i.items:
            if j.rdtype == 1: #预防CNAME错误
                iplist.append(j.address) #追加到iplist
            else:
                pass
    return True
def checkip(ip):
    checkip = ip+":80"
    getcontent = ""
    httplib.socket.setdefaulttimeout(5) #定义http连接超时时间
    conn=httplib.HTTPConnection(appdomain)#创建http连接对象
    try:
         conn.request("GET","/",headers = {"HOST": appdomain})#发起url请求
        r = conn.getresponse()
        getresponse = r.read(15) #获取UTL前15个字符
    finally:
        if getresponse == "<!DOCTYPE html>": #监控URL内容
            print ip +" [OK]"
        else:
            print ip +" [ERROR]"
if __name__=="__main__":
    if get_iplist(appdomain) and len(iplist) > 0: #域名解析正确且至少返回一个IP
        for ip in iplist:
            checkip(ip)
    else:
        print "dns reslover error"
