# coding=utf-8

'''
Created on 2021-10-15

@author: Administrator
'''
#To generate hash.txt
#Author:RobotGF

import string
import hashlib
import random
import time
import datetime
# 选取16个随机字符串加密
def genHash():
    raw_pwd="".join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*1234567890',16)).replace(' ','')
    m = hashlib.md5()
    m.update(raw_pwd.encode("UTF8"))
    cry_pwd = m.hexdigest()
    print(cry_pwd)
    return cry_pwd

#获取当天的日期
def getToday():
    t=datetime.datetime.now()
    #当前日期
    d1 =t.strftime('%Y-%m-%d')
    return d1

#获取numday天后日期
def getNday(numday):
    t=datetime.datetime.now()
    d7=(t+datetime.timedelta(days=numday)).strftime("%Y-%m-%d")
    return d7