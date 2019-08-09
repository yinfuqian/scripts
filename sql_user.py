#!/usr/bin/python 
#coding=utf-8
#grant mysql 
#创建者 Larryd
#时间 2019/06/21
print "##############################################"
print "#          在执行此脚本前请先执行            #"
print "######       pip install pymysql      ########"
print "##############################################"
import time 
print "##############################################"
print "# 请按Ctrl+C停止此脚本执行上述命令后再次运行 #"
print "#             否则运行可能出现错误           #"
print "#            如已安装 请忽略继续执行         #"
print "##############################################"
time.sleep(2)
import os 
import shutil
import pymysql
import re
import sys
import getpass
[Y,y] = ["Y", "y"]
def ip_check():
	def judge(host2):
		com_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
		if com_ip.match(host2):
        		return True 
		else:
		        return False
	if __name__=='__main__':
        	host2=raw_input ("请再次输入:")
        	if judge(host2):
        		pass
		else:
			print "输入错误，即将返回···"
			time.sleep(1)
			admin()
def admin():
	db = raw_input ("输入需要连接/授权的数据库：")
	req2 = raw_input ("数据库是否在本地Y/N：")
	if req2 == "Y" or req2 == "y":
		host = "127.0.0.1"
		user = "root"
	elif req2 =="N" or req2 == "n":
		user = raw_input ("请输入数据库登录用户：")
                r_user = raw_input ("请再次输入:")
                if (user != r_user):
                        print ("两次输入不一致···")
                        admin()
		host = raw_input ("请输入需要连接的数据库的主机IP：")
		ip_check()
	else:
		print "输入错误，即将退出···"
		time.sleep(2)
		sys.exit()
	passwd = getpass.getpass ("请输入数据库连接密码：")
	conn = pymysql.connect(host, user, passwd, db)	
	print "数据库连接成功"
	host2 = raw_input ("请输入需要授权的IP：")
	ip_check()
        user2 = raw_input ("请输入您想授权的用户:")
	r_user2 = raw_input ("请再次输入:")
	if (user2 != r_user2):
		print ("两次输入不一致···")
 		admin()
        passwd2 = raw_input ("请输入数据库授权密码：")
        print "请输入您想授权的权限···"
        print "################################"
        print "#### 1: 查询         2: 插入####"
        print "#### 3: 更新         4：删除####"
        print "#####5: 所有         6: 退出####"
        print "################################"
        while True:
                a = raw_input("请输入你的选择:")
                if a == "1":
                        cur = conn.cursor()
                        sql = '' "grant select ON *.* to %s@%s identified by %s"
			cur.execute(sql,(user2,host2,passwd2))
			conn.commit()
                        print "操作成功···"
		
                elif a == "2":
                        cur = conn.cursor()
                        sql = '' "grant insert ON *.* to %s@%s identified by %s"
			cur.execute(sql,(user2,host2,passwd2))
			conn.commit()
                        print "操作成功···"
                elif a == "3":
                        cur = conn.cursor()
                        sql = '' "grant update ON *.* to %s@%s identified by %s"
			cur.execute(sql,(user2,host2,passwd2))
			conn.commit()
                        print "操作成功···"
                elif a == "4":
                        cur = conn.cursor()
                        sql = '' "grant delete ON *.* to %s@%s identified by %s"
			cur.execute(sql,(user2,host2,passwd2))
			conn.commit()
                        print "操作成功···"
                elif a == "5":
                        cur = conn.cursor()
                        sql = '' "grant all privileges ON *.* to %s@%s identified by %s"
			cur.execute(sql,(user2,host2,passwd2))
			conn.commit()
                        print "操作成功···"
                elif a == "6":
			sys.exit()
		else:	
			print "输入错误，请重新输入···"
                        continue
		sql  = "flush privileges;"
		cur.execute(sql)	
admin()	

