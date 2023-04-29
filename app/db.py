#coding=utf-8
'''
Created on 2022-7-24

@author: superkb1
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
sys.path.append("../")  # 将另外一个目录加入环境变量
from config import Config
MYSQLURI=Config.MYSQLURI

SQLALCHEMY_DATABASE_URI = MYSQLURI
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追踪数据的修改信号
SQLALCHEMY_ECHO = True

def db():
    db=SQLAlchemy()
    return db
