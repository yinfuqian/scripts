#!/usr/bin/python
#encoding=utf8
import pycurl
import os,sys
import time
import sys
URL="http://www.baidu.com"
c = pycurl.Curl()                                      # 创建url对象
c.setopt(pycurl.URL, URL)                              #定义url常量
c.setopt(pycurl.CONNECTTIMEOUT, 5)                     #定义请求连接的等待时间     
c.setopt(pycurl.TIMEOUT, 5)                            #定义超时时间
c.setopt(pycurl.NOPROGRESS, 1)                         #屏蔽下载进度条
c.setopt(pycurl.FORBID_REUSE, 1)                       #完成交互后强制断开连接
#c.setopt(pycurl.MAXREDIRS, 1)                         #强制断开获取新的连接，替代缓存中的连接
c.setopt(pycurl.FRESH_CONNECT, 1)                      #指定HTTP重定向的最大数
c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
"""
c.setopt(pycurl.URL,"http://www.baidu.com")            #指定请求的URL
#指定HTTP头文件
c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36")
c.setopt(pycurl.HEADERFUNCTION, getheader)            #将返回的HTTP HEADER 定向到回调函数getheader
c.setopt(pycurl.WRITEFUNCTION, getbody)               #将返回的内容定向到回调函数getbody
c.setopt(pycurl.WRITEHEADER, fileobj)                 #将返回的HTTP HEADER定向到fileobj文件对象
c.setopt(pycurl.WRITEDATA, fileobj)                   #将返回的HTML内容定向到fileobj文件对象
c.getinfo(pycurl.HTTP_CODE)                           #返回HTTP状态码
c.getinfo(pycurl.NAMELOOKUP_TIME)                     #创数结束所消耗的总时间
c.getinfo(pycurl.CONNECT_TIME)                        #建立连接所消耗的时间
c.getinfo(pycurl.PRETRANSFER_TIME)                    #从建立连接到准备传输所消耗的时间
c.getinfo(pycurl.STARTTRANSFER_TIME)                  #从建立连接到传输开始所消耗的时间
c.getinfo(pycurl.REDIRECT_TIME)                       #重定向所消耗的时间
c.getinfo(pycurl.SIZE_UPLOAD)                         #上传数据包的大小
c.getinfo(pycurl.SIZE_DOWNLOAD)                       #下载数据包的大小
c.getinfo(pycurl.SPEED_DOWNLOAD)                      #平均下载速度
c.getinfo(pycurl.SPEED_UPLOAD)                        #平均上传速度
c.getinfo(pycurl.HEADER_SIZE)                         #HTTP头部文件
"""
indexfile = open(os.path.dirname(os.path.realpath(__file__))+"/content.txt","wb")
c.setopt(pycurl.WRITEHEADER, indexfile)
c.setopt(pycurl.WRITEDATA, indexfile)
try:
    c.perform()
except Exception,e:
    print "connetion error:" + str(e)
    indexfile.close()
    c.close()
    sys.exit()
NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)
CONNECT_TIME = c.getinfo(c.CONNECT_TIME)
PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)
STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
HTTP_CODE = c.getinfo(c.HTTP_CODE)
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)
HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)
#打印相关数据
print "HTTP状态码: %s" %(HTTP_CODE)
print "DNS解析时间:%.2f ms"%(NAMELOOKUP_TIME*1000)
print "建立连接时间:%.2f ms"%(CONNECT_TIME*1000)
print "准备传输时间:%.2f ms"%(PRETRANSFER_TIME*1000)
print "传输开始时间:%.2f ms"%(STARTTRANSFER_TIME*1000)
print "传输结束总时间:%.2f ms"%(TOTAL_TIME*1000)
print "下载数据包大小:%d bytes/s"%(SIZE_DOWNLOAD)
print "HTTPT头部大小:%d byte"%(HEADER_SIZE)
print "平均下载速度:% d bytes/s"%SPEED_DOWNLOAD
#关闭文件和url
indexfile.close()
c.close
