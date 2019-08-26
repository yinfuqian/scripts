#!/usr/bin/python
#encoding=utf8
#from __future__ import unicode_literals 
from fabric.api import *

env.user = 'root'
env.host = '47.100.239.107'
env.password = 'fs.com1020'

@runs_once
def local_task():
        local("uname -a")

def remote_task():
        with cd ("/usr/local/"):
                run("ls -l")
