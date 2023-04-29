# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'robot.env'))


class Config(object):
    # 配置文件设置
    maxlistadmin = os.environ.get('maxlistadmin')
    String_list = os.environ.get('String_list')

    YunHanshu = os.environ.get('YunHanshu')
    MYSQLURI = os.environ.get('MYSQLURI')


    HOST=os.environ.get('HOST')
    USER=os.environ.get('USER')
    PORT=os.environ.get('PORT')
    PASSWORD=os.environ.get('PASSWORD')
    DBNAME=os.environ.get('DBNAME')
