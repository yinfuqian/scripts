#!/usr/bin/env python
#coding=utf-8
#mongo 批量插入
import time,datetime

import random

import pymongo

from pymongo import MongoClient

client = MongoClient('mongodb://47.100.239.107:27017/test') 

db = client.test

def func_time(func):

    def _wrapper(*args,**kwargs):

        start = time.time()

        func(*args,**kwargs)

        print func.__name__,'run:',time.time()-start

    return _wrapper

 

#@func_time
def randy():
    rand = random.randint(1,1000000)
    return rand
@func_time
def mread(num):
    find = db.userinfo
    for i in range(num):
        rand = randy()
        #随机数查询
        find.find({"author": str(rand)+"Mike"})
        if i%100000 == 0:
            print "find %s ."%i
if __name__ == "__main__":
    #设定循环100万次
    num = 1000000
    mread(num)
