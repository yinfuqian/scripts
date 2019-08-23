#!/bin/bash
#Larryd
#2019.8.6
#Zabbix 安装
#环境检查
mp=`netstat -tanlp |grep mysql |awk -F : '{print $4 }'`
release=`cat /etc/redhat-release`
selinux=`getenforce 0`
firewalld=`systemctl status firewalld |grep Active |awk '{print $3}' `
hdir=`grep DocumentRoot /etc/httpd/conf/httpd.conf |grep html |awk -F '"' '{print $2}'`
echo "mysql端口为:$mp"
echo "内核版本为:$release"
echo "selinux状态为:$selinux"
echo "firewalld状态为:$firewalld"
echo "##################################"
echo "##########   请选择版本     ######"
echo "### 1:3.0                2:4.0 ###"
echo "##################################"
read -p "输入需要安装的版本1/2：" version
#wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
#sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
#yum install -y OpenIPMI ipmitool
read -p "请输入连接mysql的用户：" user
stty -echo #隐藏回显
read -p  "请输入连接mysql的密码:" pass
datadir=` mysql -u$user -p$pass -e "show variables like '%datadir%'" >/dev/null 2>&1| grep datadir | awk '{print $2}'` 
cd $datadir 
cd zabbix >/dev/null 2>&1
#创建zabbix库
if [ $? -eq 0 ];then
        rm -rf $datadir/zabbix
fi
mysql -u$user -p$pass -e 'create database zabbix character set utf8 collate utf8_bin;'>/dev/null 2>&1 
mysql -u$user -p$pass -e 'grant all privileges on *.*  to zabbix@localhost identified by "zabbix";'>/dev/null 2>&1
stty echo
#rpm下载
if [ $version -eq 2 ];then
	rpm -ivh http://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-2.el7.noarch.rpm >/dev/null
	yum install zabbix40-web-mysql.noarch zabbix40-server-mysql.x86_64 -y >/dev/null
elif [ $version -eq 1 ];then
	rpm -ivh http://repo.zabbix.com/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm >/dev/null
fi 
#导入数据
if [ $? -eq 0 ];then
	cd /usr/share/zabbix-mysql 
        mysql -uzabbix -pzabbix -hlocalhost zabbix < schema.sql >/dev/null 2>&1
        mysql -uzabbix -pzabbix -hlocalhost zabbix < images.sql >/dev/null 2>&1
        mysql -uzabbix -pzabbix -hlocalhost zabbix < data.sql >/dev/null 2>&1
else 
	echo "rpm包下载错误"
	exit
fi 
#设置时区
sed -i.ori '18a php_value date.timezone  Asia/Shanghai' /etc/httpd/conf.d/zabbix.conf
#解决中文乱码
yum -y install wqy-microhei-fonts
cp /usr/share/fonts/wqy-microhei/wqy-microhei.ttc /usr/share/fonts/dejavu/DejaVuSans.ttf >/dev/null 2>&1

#网页安装
cd $hdir
mkdir zabbix >/dev/null
cp /usr/share/zabbix/* zabbix/ >/dev/null 2>&1
ls $hdir/zabbix/ >/dev/null
if [ $? -eq 0 ];then
	echo "#################################################" 
	echo "###*                                         *###" 
	echo "###* 访问域名/ip + /zabbix/setup进行网页安装 *###"
	echo "###*                                         *###" 
	echo "#################################################" 
else 
	echo "安装失败"
	exit
fi

