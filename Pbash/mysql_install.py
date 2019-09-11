#!/usr/bin/python
#coding=utf-8
#Larryd.Yin
#mysql安装
import commands
import os  
import shutil
import time
import sys
#参数定义
[A,B,C,a,b,c,R,r] = ["A","B","C","a","b","c","R","r"]
m_name = "mysql-5.5.62-linux-glibc2.12-x86_64.tar.gz"
m2_name = "mysql-5.6.44-linux-glibc2.12-x86_64.tar.gz"
m3_name = "mysql-5.7.26-linux-glibc2.12-x86_64.tar"
m_p = "/usr/local/mysql"
m_fp = "/etc/my.cnf"
#service管理
def jnsystem():
    os.chdir("/usr/local/mysql")
    os.mkdir ("log")
    if os.path.isfile('/usr/local/mysql/log/error.log') == True:
         pass
    else:
        os.mknod("/usr/local/mysql/log/error.log")
    commands.getstatusoutput("chown -R mysql:mysql /usr/local/mysql/*")
    shutil.copy("support-files/mysql.server","/etc/init.d/mysql")
    os.chdir ("/usr/local/mysql")
    commands.getstatusoutput("rm -rf my.cnf")
    f = 'my.cnf'
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
#环境清理
def clean():
    print "环境清理中···"
    commands.getstatusoutput(" yum erase mariadb mariadb-server mariadb-libs mariadb-devel -y")
    commands.getstatusoutput("yum remove mariadb -y ")
    commands.getstatusoutput("yum -y install make gcc-c++ cmake bison-devel  ncurses-devel perl ")
    commands.getstatusoutput("groupadd mysql && useradd -r -g mysql -s /bin/fales mysql")
#版本5安装
def mysql5():
    clean()
    os.chdir ("/usr/local")
    print "准备安装···"
    if os.path.isfile(m_name) == True:
        print "本地已经存在5.5.gz无需下载"
    else:
        commands.getstatusoutput("wget https://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.62-linux-glibc2.12-x86_64.tar.gz")
    print "正在解压安装包···"
    commands.getstatusoutput("tar vzxf mysql-5.5.62-linux-glibc2.12-x86_64.tar.gz")
    shutil.move("mysql-5.5.62-linux-glibc2.12-x86_64","mysql")
    os.chdir ("/usr/local/mysql")
    print "开始安装···"
    print "时间较久，请耐心等候···"
    commands.getstatusoutput("./scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql/ --datadir=/usr/local/mysql/data")    
    jnsystem() #调用service
#版本6 安装
def mysql6():
    	clean()
        os.chdir ("/usr/local")
        print "准备安装···"
        if os.path.isfile(m2_name) == True:
                print "本地已经存在5.6.gz无需下载"
        else:
                commands.getstatusoutput("wget https://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.44-linux-glibc2.12-x86_64.tar.gz")
        print "正在解压安装包···"
        commands.getstatusoutput("tar vzxf mysql-5.6.44-linux-glibc2.12-x86_64.tar.gz")
        commands.getstatusoutput("rm -rf mysql")
        shutil.move("mysql-5.6.44-linux-glibc2.12-x86_64","mysql")
        os.chdir ("/usr/local/mysql")
        print "开始安装···"
        print "时间较久，请耐心等候···"
        commands.getstatusoutput("./scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql/ --datadir=/usr/local/mysql/data")
        jnsystem()
#版本7 安装
def mysql7():
    	clean()
        os.chdir ("/usr/local")
        print "准备安装···"
        if os.path.isfile(m3_name) == True:
                print "本地已经存在5.7.26无需下载"
        else:
                commands.getstatusoutput("wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.26-linux-glibc2.12-x86_64.tar")
        print "正在解压安装包···"
        commands.getstatusoutput("tar xf mysql-5.7.26-linux-glibc2.12-x86_64.tar")
        commands.getstatusoutput("tar xf mysql-5.7.26-linux-glibc2.12-x86_64.tar.gz")
        commands.getstatusoutput("rm -rf mysql")
        shutil.move("mysql-5.7.26-linux-glibc2.12-x86_64","mysql")
        os.chdir ("/usr/local/mysql")
        print "开始安装···"
        print "时间较久，请耐心等候···"
        commands.getstatusoutput("chown -R  mysql:mysql /usr/local/mysql/*")
        commands.getstatusoutput("./bin/mysqld --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data")
        jnsystem()
def methods():
    print "#############################################################"
    print "######################  启动方式 ############################"   
    print "#############################################################"
    print "####                                                   ######"
    print "##############  /etc/init.d/mysql starst  ###################"
    print "####                                                   ######"
    print "########################  或者  #############################"
    print "####                                                   ######"
    print "#### /usr/local/mysql/support-files/mysql.server start ######"
    print "####                                                   ######"
    print "#############################################################"
    print "####### 如有错误~ 请查看/usr/log/mysql/log/error.log ########"
    print "#############################################################"
def Minstall():
    print "###############可安装版本###############"
    print "###### A :5.5    B :5.6  C: 5.7 ########"
    print "################   R：返回 #############"
    print "########################################"
    while True:
        Inp = raw_input ("请输入你的选择A/B/C:")
        if Inp == A or Inp == a:
            mysql5()
        elif Inp == B or Inp == b:
            mysql6()
        elif  Inp == C or Inp == c:
                mysql7()
        elif Inp == R or Inp == r:
            function()
        else:
            print "输入错误，请重新输入"
            continue     
        print "安装成功"
        time.sleep(1)
        print "启动方式如下:"
        methods()        
        time.sleep(5)
        print "感谢使用···"
        sys.exit()
def Mremove():
    if os.path.isdir(m_p) == True:
        shutil.rmtree(m_p)
    else:
        print "没有mysql目录···"
    if os.path.isfile(m_fp) == True:
        os.remove("/etc/my.cnf")
    else:
        print "没有my.cnf文件···"    
    commands.getstatusoutput("userdel mysql")
    print "成功删除···"
def function():
    print "################## A 安装 ################"
    print "################## B 卸载 ################"
    while True:
        inp = raw_input ("请选择选项:")
        if inp == A or inp == a:
            Minstall()
        elif inp == B or inp == b:
            Mremove()
            sys.exit()
        else:
            print "输入错误···"
            continue
function()
