#!/usr/bin/python
#coding=utf-8
#mongo查询时间消耗
import time,datetime
import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://47.100.239.107:27017/test') 
db = client.test
#from pymongo import Connection
#connection = Connection('127.0.0.1', 27017)
#db = connection['test']
#时间记录器
def func_time(func):

    def _wrapper(*args,**kwargs):

        start = time.time()

        func(*args,**kwargs)

        print func.__name__,'run:',time.time()-start

    return _wrapper



@func_time

def insert(num):

    posts = db.userinfo

    for x in range(num):

        post = {"_id" : str(x),

            "author": str(x)+"Mike",

            "description1":"this is a very long description for " + str(x),

            "description2":"this is a very long description for " + str(x),

            "description3":"this is a very long description for " + str(x),

            "description4":"this is a very long description for " + str(x),

            "description5":"this is a very long description for " + str(x),

            "text": "My first blog post!",

            "tags": ["mongodb", "python", "pymongo"],

            "date": datetime.datetime.utcnow()}

        posts.insert_one(post)

        if x%100000 == 0:

            print "100000 !  --  %s"%(datetime.datetime.now())



if __name__ == "__main__":

#设定循环1000万次

    num = 10000000

    insert(num)
