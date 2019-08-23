#!/usr/bin/python
#encoding=utf8
import pexpect
import sys
c = pexpect.spawn('ssh root@127.0.0.1')
fout = file('log.txt','w')
c.logfile = fout
#c.log = sys.stdout
c.expect("password:")
c.sendline("fs.com1020")
c.expect('#')
c.sendline('ls /home')
c.expect('#')
# ssh 登录并执行ls 写入log文件中
