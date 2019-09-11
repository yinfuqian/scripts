#!/usr/bin/python
#encoding=utf8
#from __future__ import unicode_literals 
from fabric.api import *

env.user = "root"
env.hosts = "47.100.239.107"
env.password = "fs.com1020"

@runs_once   #主机遍历过程中只有第一台触发此函数
def input_raw():
	return prompt("plese input dir name:",default="/home")

def worktask(dirname):
	run("ls -l "+dirname)

@task  #限定只有go函数对fab命令可见
def go():
	getdirname = input_raw()
	worktask(getdirname)
