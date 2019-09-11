#!/usr/bin/python3
#coding=utf-8
#Yin
#lamp安装
import sys
import shutil
import commands
import os
import time
#参数定义

conf_path = "/etc/httpd/conf/httpd.conf"
path_re = (os.path.isfile(conf_path))
in_path = "/usr/local"
h_name = "httpd-2.4.39.tar.gz"
h_path = "/usr/local/httpd"
dir_re = (os.path.isdir(h_path))
m2_name = "mysql-5.6.44-linux-glibc2.12-x86_64.tar.gz"
m_p = "/usr/local/mysql"
m_fp = "/etc/my.cnf"

def Minstall():
	os.system("cd /usr/local")
	print "=============正在解压安装包============"
	os.system("tar xf mysql-5.6.44-linux-glibc2.12-x86_64.tar.gz")
	os.system("rm -rf mysql")
	shutil.move("mysql-5.6.44-linux-glibc2.12-x86_64","mysql")
	os.chdir("/usr/local/mysql")
	print "================开始安装==============="
	print "=========时间较久，请耐心等候···======="
	time.sleep(1)
	os.system("./scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql/ --datadir=/usr/local/mysql/data")
	#os.chdir("/usr/local/mysql")
	os.system("rm -rf log")
	os.mkdir ("log")
#创建日志文件
	if os.path.isfile('/usr/local/mysql/log/error.log') == True:
		os.chdir("/usr/local/mysql")
		os.system("chown -R mysql:mysql /usr/local/mysql/*")
		shutil.copy("support-files/mysql.server","/etc/init.d/mysql")
		os.chdir ("/usr/local/mysql")
		os.system("rm -rf my.cnf")
	else:
		os.chdir("/usr/local/mysql")
		os.system("touch /usr/local/mysql/log/error.log")
		os.system("chown -R mysql:mysql /usr/local/mysql/*")
		shutil.copy("support-files/mysql.server","/etc/init.d/mysql")
		os.chdir ("/usr/local/mysql")
		os.system("rm -rf my.cnf")
	f = 'my.cnf'
#生成mysql主配置文件
	with open(f,"w") as h_file:
		h_file.write('[mysqld]'
		'\nbasedir=/usr/local/mysql'
		'\ndatadir=/usr/local/mysql/data'
		'\nsocket= /tmp/mysql.sock'
		'\nlong_query_time=2'
		'\n[mysqld_safe]'
		'\nlog-error=/usr/local/mysql/log/error.log'
		'\nlog=/usr/local/mysql/log/mysql.log')
	f2 = '/etc/profile'
	with open(f2,"a") as h2_file:
		h2_file.write('export PATH=$PATH:/usr/local/mysql/bin')
	Apache()
def pags():
	os.chdir("/usr/local")
	if os.path.isfile(h_name) == True:
		print ("==================本地已经存在2.4.gz无需下载==============")
		os.system("tar xf httpd-2.4.39.tar.gz")
	else:
		os.system("wget https://mirrors.tuna.tsinghua.edu.cn/apache/httpd/httpd-2.4.39.tar.gz")
	while True:
		if os.path.isfile("php-5.6.4.tar.gz") == True:	
			print ("===============本地存在php-5.6.gz=================")
			os.system("tar xf php-5.6.4.tar.gz")
			mysql6()
		else:	
			os.system("wget https://www.php.net/distributions/php-5.6.4.tar.gz")
			os.system("tar xf php-5.6.4.tar.gz")
			mysql6()
#apache 编译
def Ainstall():
	os.chdir("/usr/local/httpd-2.4.39")
	os.system("./configure --prefix=/usr/local/httpd --enable-so --enable-rewrite --enable-charset-lite --enable-cgi --with-mpm=prefork")
	os.system("make >/dev/null 2> &1 && make install > /dev/null 2>&1")
	print ("====================正在添加到 service 管理=======================")
#编辑service文件
	os.chdir=("/lib/systemd/system")
	os.system("rm -rf httpd.service")
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
	os.system("ln -s /usr/local/httpd/bin/apachectl /usr/local/bin/apachectl >/dev/null 2>&1")
	os.system(' sed -i "s/^:.*//" /etc/hosts')
	os.system('sed -i "s/#ServerName www.example.com:80/ServerName www.example.com:80/g" /usr/local/httpd/conf/httpd.conf')
	os.system('sed -i "209s/Require all denied/Require all granted/g" /usr/local/httpd/conf/httpd.conf ')
	os.system('sed -i "258s/DirectoryIndex index.html/DirectoryIndex index.html index.html/g" /usr/local/httpd/conf/httpd.conf')
	os.system('sed -i "396a AddType application/x-httpd-php .php" /usr/local/httpd/conf/httpd.conf')

#apache 安装
def Aprint():
	print ("======================================================")
	print ("===============APACHE INSTALL SUCCESS=================")
	print ("======================================================")
	
def Apache():
	if path_re == True:
		os.system("rm -rf /etc/httpd/httpd.conf")
	else:
		os.system("yum -y install apr apr-devel cyrus-sasl-devel expat-devel libdb-devel openldap-devel apr-util-devel apr-util pcre-devel pcre > /dev/null 2>&1 ")
		print ("===============本次安装的APACHE版本为2.4==============")
		time.sleep(1)
		os.chdir("/usr/local")
		print ("=============安装中========")
		time.sleep(1)
		if dir_re == True:
			os.system("rm -rf /usr/local/httpd")
			Ainstall()
			if os.path.isfile("/usr/local/httpd/bin/apx"):
				Aprint()
			else:
				pass
		else:
			Ainstall()
			if os.path.isfile("/usr/local/httpd/bin/apx"):
				Aprint()	
			else:
				Aprint()
	php()
def mysql6():
	os.chdir (in_path)
	os.system("cd /usr/local")
	print "====================环境清理中=================="
	print "==================mysql版本为5.6================="
	os.system(" yum erase mariadb mariadb-server mariadb-libs mariadb-devel -y >/dev/null 2>&1")
	os.system("yum remove mariadb -y >/dev/null >/dev/null 2>&1")
	os.system("yum -y install make gcc-c++ cmake bison-devel  ncurses-devel perl >/dev/null 2>&1 ")
	os.system("groupadd mysql && useradd -r -g mysql -s /bin/fales mysql >/dev/null 2>&1")
	os.system("yum -y install autoconf >/dev/null 2>&1")
	print "准备安装···"
	if os.path.isfile(m2_name) == True:
		print "==================本地已经存在5.6.gz无需下载==============="
		Minstall()
	else:
		os.system("wget https://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.44-linux-glibc2.12-x86_64.tar.gz")
		Minstall()

#php安装
def php():

	print ("==============开始安装PHP=========")
	time.sleep(1)
	os.system("yum install -y epel-release && yum install -y libmcrypt-devel")
	os.system("yum -y install gcc gcc-c++ libxml2 libxml2-devel bzip2 bzip2-devel  openssl openssl-devel libcurl-devel libjpeg-devel libpng-devel freetype-devel readline readline-devel libxslt-devel perl perl-devel psmisc.x86_64 recode >/dev/null 2>&1")
	f0 = '/tmp/install.sh'
	with open (f0,"w") as p_file1:
		p_file1.write('#!/bin/bash'
		'\n cd /usr/local/php-5.6.4'
		'\n ./configure --prefix=/usr/local/php5 --sysconfdir=/etc/php5 --with-apxs2=/usr/local/httpd/bin/apxs --with-config-file-path=/etc/php5 --enable-fpm   --with-mysql=mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd  --with-openssl --with-zlib  --with-curl  --with-jpeg-dir --with-png-dir --enable-sockets'
#		'\n./configure --prefix=/usr/local/php5 --sysconfdir=/etc/php5 --with-config-file-path=/etc/php5 --with-apx2=/usr/local/httpd/apxs --with-mysql --enable-fpm'
		'\nmake'
		'\nmake install')
	os.system("/usr/bin/bash /tmp/install.sh >/dev/null 2>&1")
	shutil.copy("/etc/php5/php-fpm.conf.default", "/etc/php5/php-fpm.conf")
	shutil.copy("/usr/local/php-5.6.4/php.ini-production", "/etc/php5/php.ini")
#	shutil.copy("/etc/php5/php-fpm.d/www.conf.default", "/etc/php5/php-fpm.d/www.conf")
	os.system(" sed -i 's%;pid = run/php-fpm.pid%pid = run/php-fpm.pid%g' /etc/php5/php-fpm.conf")	
	f1 = "/etc/profile.d/web.sh "
	with open(f1,"w") as p_file:
		p_file.write('export PATH=$PATH:/usr/local/php5/sbin:/usr/local/php5/bin')
#service 管理
#	os.chdir("/usr/lib/systemd/system")
	f2 = '/usr/lib/systemd/system/php-fpm.service'
	with open(f2,"w") as p_file2:
		p_file2.write('[Unit]'
		'\nDescription=php-fpm'
		'\nAfter=syslog.target network.target'
		'\n[Service]'
		'\nType=forking'
		'\nPIDFile=/usr/local/php5/var/run/php-fpm.pid'
		'\nExecStart=/usr/local/php5/sbin/php-fpm'
		'\nExecReload=/bin/kill -USR2 $MAINPID'
		'\nPrivateTmp=true'
		'\n[Install]'
		'\nWantedBy=multi-user.target')
	print ("===============================")
	print ("=====LAMP INSTALL SUCCESS======")
	print ("===============================")
	print ("===========服务管理============")	
	print ("=====mysql:init php:system=====")
	print ("===========Apache:system=======")
	time.sleep(1)
	sys.exit()	
pags()
