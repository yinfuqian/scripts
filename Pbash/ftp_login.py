#!/usr/bin/python
#encoding=utf8
from __future__ import unicode_literals #使用unicode编码
import pexpect
import sys
c = pexpect.spawn('ftp 127.0.0.1')	#运行ftp
c.expect('(?i)name .*:')  		#（?i）表示后面忽略大小写
c.sendline('ftptest')			#ftp账号
c.expect('(?i)password')		#匹配密码输入提示
c.sendline('123123')	#ftp密码
c.expect('ftp>')
c.sendline('bin')			#启动二进制传输模式
c.expect('ftp>')
c.sendline('get robots.txt')		#下载robots.txt
c.expect('ftp>')
sys.stdout.write (c.before)		#输出匹配“ftp>” 之前得输入和输出
print ("Escape character is '^]'.\n")
sys.stdout.write (c.after)
sys.stdout.flush()
c.interact()				#调出interact()让出控制权，用户可以继续当前会话手工控制程序，默认输入"^]跳出
