#!/usr/bin/env python

#coding=utf-8
#mongo批量插入
import multiprocessing,random,string  

import time,datetime

import pymongo

from pymongo import MongoClient

 

 

def gen_load(x,taskid): 

    client = MongoClient('mongodb://47.100.239.107:27017/test') 

    db = client.test

    posts = db.userinfo

    for x in range(1000000):

        post = {"_id" : str(x),

                "author": str(x)+"Mike",

                "text": "My first blog post!",

                "tags": ["mongodb", "python", "pymongo"],

                "date": datetime.datetime.utcnow()}

        posts.insert_one(post)

        if x%1000000 == 0:

            print "100000 !  --  %s"%(datetime.datetime.now())

 

 

if __name__ == '__main__':

    inser_number=2500

    pro_pool = multiprocessing.Pool(processes=100) 

    print time.strftime('%Y-%m-%d:%H-%M-%S',time.localtime(time.time())) 

    start_time=time.time() 

    manager = multiprocessing.Manager() 

    for i in xrange(10): 

            taskid=i   

            pro_pool.apply_async(gen_load,args=(inser_number,taskid))  

    pro_pool.close() 

    pro_pool.join() 

    elapsed = time.time()-start_time 

    print elapsed 

    time.sleep(1) 

    print "Sub-process(es) done." 
