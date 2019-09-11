#!/usr/bin/python
#coding=utf-8
#backup mysql
#创建者 Larryd
#时间 2019/06/24
#mysql 的备份和恢复
print ("##############################################")
print ("#          在执行此脚本前请先执行            #")
print ("######       pip install pymysql      ########")
print ("##############################################")
import time
print ("##############################################")
print ("# 请按Ctrl+C停止此脚本执行上述命令后再次运行 #")
print ("#             否则运行可能出现错误           #")
print ("#            如已安装 请忽略继续执行         #")
print ("##############################################")
#time.sleep(2)
import os
import pymysql
import re
import sys
import getpass
import commands
import linecache
#数据库连接以及选项
def admin():
	db = "mysql"
	req2 = raw_input ("数据库是否在本地Y/N：")
	if req2 == "Y" or req2 == "y":
		host = "localhost"
		user = "root"
		passwd = getpass.getpass("请输入数据库连接密码:")
		try:
			conn = pymysql.connect(host, user, passwd, db)
		except:
			print ("密码错误，连接失败···")
			admin() 
		print("本地数据库可以连接···")
	elif req2 =="N" or req2 == "n":
		user = raw_input ("请输入数据库登录用户：")
		r_user = raw_input("请再次输入:")
		if user != r_user:
			print ("两次输入不一致···")
			admin()
		#检测用户输入的ip格式是否正确
		def judge(host2):
                        com_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
                        if com_ip.match(host2):
                                return True
                        else:
                            return False
                if __name__=='__main__':
                      #测试远程数据库是否可以连接 
			host2=raw_input("请输入需要操作的mysql主机IP：")
                        if judge(host2):
                                pass
                        else:
                                print ("输入错误，即将返回···")
				admin()
		passwd = getpass.getpass("请输入数据库连接密码:")
		try:
			conn = pymysql.connect(host2, user, passwd,db)
                except:
                        print ("账户密码密码错误，连接失败···")
                        admin()
		print("数据库可以连接···")
		time.sleep(1)
	else:
		print("输入错误···即将退出")
		sys.exit()
	while True:
		print("###########################")
		print("###  1 备份       2 恢复###")
		print("#######    3 退出   #######")
		print("###########################")
		chose = raw_input("请选择你的操作1/2/3:")
		if chose == "1":
        		db2 =raw_input("输入你想备份数据库名称：")
        		cursor= conn.cursor()
			#创建一个文件写入datadir
			commands.getstatusoutput("rm -rf /data/file.txt")
		        file = open(r'/data/file.txt', 'w')
		        sql = """show variables like '%datadir%';"""
			#错误处理，写入失败输出IndexError
		        try:
		                cursor.execute(sql)
		                results = cursor.fetchall()
		                i = 0
		                for row in results:
                        		file.write('%s :: %s\n' % (row[0],row[1]))
                		i+=1
        		except IndexError as e:
                		conn.rollback()
                		print (e)
        		file.close()
        		# 工作目录切换到数据目录
        		a = commands.getstatusoutput("awk  '{print $3}' /data/file.txt")
        		os.chdir(a[1])
			#判断输入是否为系统库
        		if os.path.isdir(db2) == True:
				if db2=="mysql" or db2=="performance_schema" or db2=="information_schema" or db2=="sys":
               				print "(输入的数据库为自带的数据库···)"
					continue
				#定义备份文件名称
				timestr = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
				folder = "/data/backup/"+db2+"."+timestr
				#创建备份目录并执行备份
				commands.getstatusoutput("mkdir /data/backup")
				dump_sql = "mysqldump -u%s -p%s %s >%s.sql"%(user, passwd, db2, folder)
				os.system(dump_sql)
				print ("导出成功/数据目录为/data/backup")
			else:
				print ("不存在这个库···")
		elif chose == "2":
			#判断输入路径是否正确
			path = raw_input ("请输入你的备份目录：")
			if os.path.isdir(path) == True:
				pass
			else:
				print ("路径输入有误···")
				admin()
			os.chdir(path)
			print ("##############################")
			print ("## 1:.gz    2:.zip   3:.sql ##")
			print ("########    4:返回主页  ######")
			print ("##############################")
			db3 = raw_input ("请选择备份文件类型1/2/3")
			while True:
				if db3 == "1":
					#判断输入是否合法
					def gjudge(num):
						num1=re.compile('^([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9)$')
						if num1.match(num):
							return True
						else:
							return False
					if __name__=='__main__':
						date = raw_input("选择你想恢复的日期月/日/时/分 如 06250909:")
						if judge(date):
							pass
						else:
							print ("输入错误，即将返回···")
							continue
					#得到备份文件的名称
					com1 = "ls %s |grep %s > /data/test.txt"%(path, date)
					os.system(com1)
					os.chdir("/data/")
					FileName = linecache.getline('test.txt',1)
					#解压得到sql文件
					com2 = "rm -rf %s/*.sql &&  tar xf %s "%(path, FileName)
					os.system(com2)
					#得到sql文件的名称
					com3 = "ls %s |grep .sql> /data/test.txt"%(path)
					os.system(com3)
					os.chdir("/data")
					sql_name = linecache.getline('test.txt',1)
					#删除已有的库后执行导入操作
					print ("再做导入操作之前，为了避免数据发生冲突，请先删除原有得数据")
					d_db = raw_input ("请输入需要删除得库名：")
					os.chdir(path)
					com4 = "mysql -u%s -p%s -e 'drop database %s;'"%(user, passwd, d_db)
					com5 = "mysql -u%s -p%s -e 'create database %s;'"%(user, passwd, d_db)
					com6 = "mysql -u%s -p%s %s< %s/%s"%(user, passwd, 'd_db', path, sql_name)
					os.system(com4)
					os.system(com5)
					os.system(com6)
					os.chdir(path)
					if os.path.isdir(c_drop) == True:
						print ("导入成功")
					else:
						print ("导入失败···")
						print ("正在返回···")
						sys.exit()
				elif db3 == "2":
                                        def judge(num):
						num1=re.compile('^([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9)$')
                                                if num1.match(num):
                                                        return True
                                                else:
                                                        return False
                                        if __name__=='__main__':
                                                date = raw_input("选择你想恢复的日期月/日/时/分 如 06250909:")
                                                if judge(num):
                                                        pass
                                                else:
                                                        print ("输入错误，即将返回···")
                                                        continue
                                        #得到所需要的备份文件名称
					com1 = "ls %s |grep %s > /data/test.txt"%(path, date)
                                        os.system(com1)
                                        os.chdir("/data/")
                                        FileName = linecache.getline('test.txt',1)
                                        #解压
					com2 = "rm -rf %s/*.sql &&  unzip  %s "%(path, FileName)
                                        os.system(com2)
                                        com3 = "ls %s |grep .sql > /data/test.txt"%(path)
                                        os.system(com3)
					os.chdir("/data")
                                        sql_name = linecache.getline('test.txt',1)
                                        print ("再做导入操作之前，为了避免数据发生冲突，请先删除原有的数据Y/N")
                                        d_db = raw_input ("请输入需要删除的库名：")
                                        com4 = "mysql -u%s -p%s -e 'drop database %s;'"%(user, passwd, d_db)
                                        com5 = "mysql -u%s -p%s -e 'create database %s;'"%(user, passwd, d_db)
                                        com6 = "mysql -u%s -p%s %s < %s/%s"%(user,passwd,path,sql_name)
					os.system(com4)
					os.system(com5)
					os.system(com6)
                                        os.chdir(path)
                                        if os.path.isdir(d_db) == True:
                                                print ("导入成功")
                                        else:
                                                print ("导入失败···")
                                                print ("正在退出···")
                                                sys.exit()
				elif db3 == "3":
                                        def judge(num):
						num1=re.compile('^([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9])$')
                                                if num1.match(num):
                                                        return True
                                                else:
                                                        return False
                                        if __name__=='__main__':
                                                date = raw_input("选择你想恢复的日期月/日/时/分 如 06250909:")
                                                if judge(date):
                                                        pass
                                                else:
                                                        print ("输入错误，即将返回···")
                                                        continue
                                        com1 = "ls %s |grep %s > /data/test.txt"%(path, date)
                                        os.system(com1)
                                        os.chdir("/data/")
                                        FileName = linecache.getline('test.txt',1)
                                        com3 = "ls %s |grep .sql > /data/test.txt"%(path)
                                        os.system(com3)
					os.chdir("/data")
                                        sql_name = linecache.getline('test.txt',1)
                                        print("再做导入操作之前，为了避免数据发生冲突，请先删除原有得数据Y/N")
                                        d_db = raw_input ("请输入需要删除得库名：")
                                        com4 = "mysql -u%s -p%s -e 'drop database %s;'"%(user, passwd, d_db)
                                        com5 = "mysql -u%s -p%s -e 'create database %s;'"%(user, passwd, d_db)
                                        com6 = "mysql -u%s -p%s %s < %s/%s"%(user, passwd, d_db,  path, sql_name)
					os.system(com4)
					os.system(com5)
					os.system(com6)
                                        os.chdir(path)
                        		cursor= conn.cursor()
                     			#创建一个文件写入本地mysql datadir
                     			commands.getstatusoutput("rm -rf /data/test.txt")
                        		file = open(r'/data/test.txt', 'w')
					#得到datadir
                        		sql = """show variables like '%datadir%';"""
                        		try:
                                		cursor.execute(sql)
                                		results = cursor.fetchall()
                                		i = 0
                                		for row in results:
                                        		file.write('%s :: %s\n' % (row[0],row[1]))
                                		i+=1
                        		except IndexError as e:
                                		conn.rollback()
                                		print (e)
                        		file.close()
                        		### 判断是否存在库文件
                        		a = commands.getstatusoutput("awk  '{print $3}' /data/test.txt")
                        		os.chdir(a[1])
                        		if os.path.isdir(d_db) == True:
                                                print ("导入成功")
						sys.exit()
                                        else:
                                                print ("导入失败···")
                                                print ("正在返回···")
						sys.exit()
				elif db3 == "4":
					admin()
				else:
					print("输入有误···")
                         		break
		elif chose == "3":
			sys.exit()
		else:
			print("输入有误···")
			continue
admin()
