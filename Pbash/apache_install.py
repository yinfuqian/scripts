#!/usr/bin/python
# coding=utf-8
import commands 
import os 
import sys
import time
conf_path = "/etc/httpd/conf/httpd.conf"
path_re = (os.path.isfile(conf_path))
in_path = "/usr/local"
h_name = "httpd-2.4.39.tar.gz"
h_path = "/usr/local/httpd"
dir_re = (os.path.isdir(h_path))
Y = "Y"
y = "y"
#if path_re == True:

def install():
#判断是否存在conf文件如果有责删除不存在继续安装
	print "存在conf文件是否删除"
	cho =raw_input ("请选择Y或者N:")
	if cho == Y or cho == y:
		os.chdir("/etc/httpd/conf/")
		commands.getstatusoutput("rm -rf httpd.conf")
		print "准备安装···"
#安装apache所需要的依赖包
		commands.getstatusoutput("yum -y install apr apr-devel cyrus-sasl-devel expat-devel libdb-devel openldap-devel apr-util-devel apr-util pcre-devel pcre")
		#time.sleep(1)
		print "本次安装的版本为2.4···"
		os.chdir("/usr/local")
		print "安装中···"
#判断是否存在gz包 如果有责不用下载继续安装，没有则先下载然后安装
		if os.path.isfile(h_name) == True:
			print "本地已经存在2.4.gz无需下载"
		else:
			commands.getstatusoutput("wget https://mirrors.tuna.tsinghua.edu.cn/apache/httpd/httpd-2.4.39.tar.gz")
#判断是否存在httpd 如果存在 判断是否先删出再安装如果没有直接安装
		while dir_re == True:
			print "存在httpd目录是否删除···"
			cho2 = raw_input ("请输入Y或者N:")
			while cho2 == y or cho2 == Y:
				commands.getstatusoutput("rm -rf /usr/local/httpd")
			else:
				print "目录存在冲突，即将退出···"
				time.sleep(1)
			continue
		else:
			print "继续安装···"
			commands.getstatusoutput("tar xf httpd-2.4.39.tar.gz")
			os.chdir("/usr/local/httpd-2.4.39")
			commands.getstatusoutput("./configure --prefix=/usr/local/httpd --enable-so --enable-rewrite --enable-charset-lite --enable-cgi")
			commands.getstatusoutput("make && make install")
			print "安装成功···"
			cho3 = raw_input ("请选择是否将httpd加入系统脚本管理Y/N:")
			if cho3 == Y or cho3 == y:
#将httpd启动脚本加system管理
				os.chdir=("/lib/systemd/system")
				commands.getstatusoutput("rm -rf httpd.service")
				f = '/lib/systemd/system/httpd.service'
				with open(f,"w") as h_file:
					h_file.write('[Unit]'
					'\nDescription=The Apache HTTP Server'
					'\nAfter=network.target'
					'\n[Service]'
					'\nType=forking'
					'\nPIDFile=/usr/local/httpd/logs/httpd.pid'
					'\nExecStart=/usr/local/bin/apachectl $OPTIONS'
					'\nExecReload=/bin/kill -HUP $MAINPID'
					'\nKillMode=process'
					'\nRestart=on-failure'
					'\nRestartSec=42s'
					'\n[Install]'
					'\nWantedBy=graphical.target')
				commands.getstatusoutput("ln -s /usr/local/httpd/bin/apachectl /usr/local/bin/apachectl")
				commands.getstatusoutput(' sed "s/^:.*//" /etc/hosts')
			else:
				sys.exit()		
	else:
		print "输入错误，退出程序····"
		sys.exit()
if path_re == True:
	install()
else:
	install()
	
