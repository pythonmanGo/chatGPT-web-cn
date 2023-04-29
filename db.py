#coding=utf-8
'''
Created on 2023年4月29日

@author: superkb1
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from config import Config
MYSQLURI=Config.MYSQLURI

SQLALCHEMY_DATABASE_URI =MYSQLURI
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追踪数据的修改信号
SQLALCHEMY_ECHO = True


db=SQLAlchemy()
   





engine = create_engine( MYSQLURI, max_overflow=0, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()