#!/usr/bin/python 
#coding=utf-8
#User Larryd 
#time 2019/06/27
#发送邮件
import yagmail
import sys
import os 
'''
user_mail:发件人邮箱
password:密码(qq邮箱是授权码的密码)
smtp_server:SMTP服务器(qq:smtp.qq.com)
recipients:收件人邮箱
subject:标题
content:邮件内容
port:端口(qq:465或587)
'''
def sed_mail(user_mail,password,smtp_server,recipients,subject,content,port=465):
	with yagmail.SMTP(user=user_mail,password=password,host=smtp_server,port=port) as yag:
		yag.send(recipients, subject, content)
user_mail = raw_input("发件人邮箱：")
passwd = raw_input("授权密码：") 
smtp = raw_input("SMTP服务器：") 
get = raw_input("收件人邮箱：") 
sub = raw_input("标题：") 
port = raw_input("端口：")
sed_mail(user_mail, passwd, smtp, get, sub, port)
