# -*- coding:utf-8 -*-
__author__ = 'superkb1'

import os
import sys

'''
系统配置文件
'''

SYSTEM_ROOT = os.path.split(os.path.realpath(sys.argv[0]))[0]

FILE_SAVE_DIR = SYSTEM_ROOT + '/' + 'data'
FILE_TEMP_DIR = SYSTEM_ROOT + '/' + 'data/temp'
FILE_LOG_DIR = SYSTEM_ROOT + '/' + 'data/log'
sys.path.append("../")  # 将另外一个目录加入环境变量
from config import Config
MYSQLURI=Config.MYSQLURI
HOST=Config.HOST
USER=Config.USER
PORT=int(Config.PORT)
PASSWORD=Config.PASSWORD
DBNAME=Config.DBNAME

DB = {
    'host':HOST,
    'user':USER,
    'password':PASSWORD,
    'port':PORT,
    'dbname':DBNAME
}

host=HOST
user=USER
port=3306
password=PASSWORD
db=DBNAME
DB_TABLENAME='chatGPT'

