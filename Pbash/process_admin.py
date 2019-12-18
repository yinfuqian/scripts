#!/usr/bin/python
#encoding=utf8
#脚本进程管理
import subprocess
import os
bash = "ps -aux |grep order |awk '{print $12}'"
fileName = "/tmp/text.txt"
flist = "order_overtime.php"
#讲ps 执行结果写入文件
def RunBash():
    outfile = open(fileName,'a')
    p = subprocess.Popen(bash, stdout=outfile, shell=True)
    if p.poll():
        return
    p.wait()
    return
#判断文件中是否存在指定内容
def files():
    fopen = open(fileName,'r')
    fileread = fopen.read()
    fopen.close()
    if flist in fileread:
        print "1"
        os.system("rm -rf /tmp/text.txt")
    else:
        print "2"
        os.system("rm -rf /tmp/text.txt")
RunBash()
files()



