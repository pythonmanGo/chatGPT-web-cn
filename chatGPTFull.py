# coding=UTF-8
'''
Created on 2023年04月29日


@author: superkb1
'''
from flask import Flask, request,  jsonify,render_template, Blueprint
from flask import make_response
import pymysql as mysql
import json
import re
import sys 
import os

import numpy as np
import pandas as pd
import app as app
import speech_recognition as sr
import cpca


from flask_oidc import OpenIDConnect
from flask import request
import hashlib
from config import Config
import os
from datetime import datetime
from email import *
from joblib import Memory
from db import db as db

import time as time


from flask_login import LoginManager,login_user, logout_user, login_required, current_user


from flask_sqlalchemy import SQLAlchemy

import pymysql as  pymysql
from sqlalchemy import create_engine
import asyncio

from aiohttp import web


from config import Config

app = Flask(__name__)
app.config.from_object(Config)

maxlistadmin=int(Config.maxlistadmin)
string_list=[]

string_list.append(Config.String_list)

YunHanshu=Config.YunHanshu
MYSQLURI=Config.MYSQLURI

print("当前openai key列表:",string_list)

app.config['SQLALCHEMY_DATABASE_URI'] = MYSQLURI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.config["SECRET_KEY"] = 'c6eaa3e917c5432ca19d033364c16b12'
#前台会话的秘钥



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from flask_bootstrap import Bootstrap
from flask import current_app      
auth = Blueprint('auth', __name__, url_prefix='/auth')

app.register_blueprint(auth)
sys.path.append("app")  # 将另外一个目录加入环境变量
from dbmanager import DB


from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from email import *
from forms import LoginForm, RegistrationForm
from flask import Flask, render_template, request, jsonify, session

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


import openai
import random
import string
import requests


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_random_number(s): 
    hashed = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) 
    if len(string_list)==1:
        hashed=0
    
    elif len(string_list)==2:
        hashed=random.randint(0, 1)
    else:
        print(hashed)
        hashed=hashed % (len(string_list)-1) 
    
    return hashed 



def answer_meg_proxy_new2(question,username,topicname):
    
    global yunhashu
    Dbman = DB()
    SQL1 = """
        SELECT t1.chatuser, t1.chatid, t1.gptouttext, t1.keyword, t2.chatuser, t2.chatid, t2.gptouttext, t2.keyword
        FROM chatgpt_info t1
        INNER JOIN chatgpt_info t2 ON t1.chatid = t2.chatid - 1
        WHERE t1.chatuser = 'user'
        AND t2.chatuser = 'assistant'
        AND LENGTH(t1.keyword) <= 0
        AND t1.username1='%s'
        and t1.topicname='%s'
        ORDER BY t1.chatid desc
        LIMIT 5;
    """%(username,topicname)
    where1=SQL1

    #取出最近5轮对话重新传入
    sourceInfotmp = Dbman.queryAll(where1)
    messageStirng=""
    result_dict = []
    i=0
    maxlen=4000-len(question)
    for row in reversed(sourceInfotmp):
        usercontent=row['gptouttext']
        botcontent=row['t2.gptouttext']
        if(len(result_dict)+len(usercontent)+len(botcontent)<maxlen):
            result_dict.append({
                'role': 'user',
                'content': usercontent
            })
            result_dict.append({
                'role': 'assistant',
                'content':botcontent
            }) 
    result_dict.append({
                'role': 'user',
                'content':question
            })      
    print("取出的结果：")    
    print(result_dict)   
    num=generate_random_number(username)
    requests.packages.urllib3.disable_warnings()
    an_info=""
    openai.api_key = string_list[num]
    
    openai.api_base =YunHanshu+ "/v1/"
    try:  
        
        response = requests.post(
            openai.api_base + "chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai.api_key}",
            },
                        
            json=
            {
             "model": "gpt-3.5-turbo-0301",
             "messages": result_dict
           },
            verify=False
    
        )     
     
        response_text = response.json()
        print(response_text)
        an_info = response_text["choices"][0]["message"]["content"].strip()

        params2 = {"username1":username,"chatuser": 'assistant',"gptouttext": an_info, "keyword": '',"jiluzt": '0','topicname':topicname}
        Dbman.insert('chatgpt_info', params_dic=params2)  
        Dbman.commit() 
    except Exception as e:
            params2 = {"username1":username,"chatuser": 'assistant',"gptouttext": '抱歉，ChatGPT负载过高,请稍后重试', "keyword": '',"jiluzt": '0','topicname':topicname}
            Dbman.insert('chatgpt_info', params_dic=params2)  
            Dbman.commit() 
            print("抱歉，ChatGPT负载过高,请稍后重试:%s" , e)
    return an_info

@app.route('/chatGPTFull', methods=['GET', 'POST'])
@login_required

def chatGPTFull(): 
    
    global maxlistadmin
    username=current_user.email
    Dbman = DB()

    sourceInfotmp=""
    topics = Dbman.selectAll(table_name='chatgpt_info',columns='topicname', where="username1 = '%s' AND jiluzt = '0' AND ( keyword IS   NULL  or length(keyword)<=0) AND topicname  IS NOT NULL  GROUP BY topicname ORDER BY chatid asc LIMIT %s "   %(username,maxlistadmin))
    topicname = request.args.get('topicname')
    print(topicname)
    if topicname!="":
        messages = Dbman.selectAll(table_name='chatgpt_info',columns='chatuser,gptouttext', where="username1 = '%s' and topicname='%s'  and  jiluzt='0'  and  ( keyword IS   NULL  or length(keyword)<=0)  order by chatid asc limit %d"  %(username,topicname,maxlistadmin))

    else:
        messages = Dbman.selectAll(table_name='chatgpt_info',columns='chatuser,gptouttext', where="username1 = '%s'   and  jiluzt='0'  and ( keyword IS   NULL  or length(keyword)<=0) order by chatid asc limit %d"  %(username,maxlistadmin))
    topicname_json = json.dumps({'topicname': topicname})
    if topicname==None:
        topicname=""
    return render_template('chatGPTFull.html',topics=topics,messages=messages,topicname=topicname)



@app.route('/chatGPTFull_chat', methods=['GET', 'POST'])
@login_required

def chatGPTFull_chat(): 
  global maxlistadmin
  username=current_user.email
  Dbman = DB()
  if request.method == 'POST':

    try:        
            data = request.get_json()        
            # 获取 message 和 topicname 值
            message = data['body']['message']
            topicname = data['body']['topicname']
            print(message)
            print("!!!!!!!!!!!!")
            if topicname=="":
                topicname=message[0:10]
            print(topicname)
            #message=parse.unquote(message)
            params1 = {"username1":username,"chatuser": 'user',"gptouttext": message,"keyword": '', "jiluzt": '0',"topicname":topicname}
            Dbman.insert('chatgpt_info', params_dic=params1)   
            Dbman.commit()
            response1 = answer_meg_proxy_new2(message,username,topicname)        
    except Exception as e:
           print(('\t抱歉，ChatGPT负载过高,请稍后重试\t%s' % e))
    sourceInfotmp=""
    topics = Dbman.selectAll(table_name='chatgpt_info',columns='topicname', where="username1 = '%s' AND jiluzt = '0' AND  ( keyword IS   NULL  or length(keyword)<=0) AND topicname  IS NOT NULL  GROUP BY topicname ORDER BY chatid asc LIMIT %s "   %(username,maxlistadmin))
    
    if topicname!="":
        messages = Dbman.selectAll(table_name='chatgpt_info',columns='chatuser,gptouttext', where="username1 = '%s' and topicname='%s'  and  jiluzt='0'  and   ( keyword IS   NULL  or length(keyword)<=0)  order by chatid asc limit %d"  %(username,topicname,maxlistadmin))

    else:
        messages = Dbman.selectAll(table_name='chatgpt_info',columns='chatuser,gptouttext', where="username1 = '%s'   and  jiluzt='0'  and   ( keyword IS   NULL  or length(keyword)<=0)  order by chatid asc limit %d"  %(username,maxlistadmin))
    if topicname==None:
        topicname=""
    return render_template('chatGPTFull.html',topics=topics,messages=messages,topicname=topicname)



@app.route('/chatGPTFull_Topicname', methods=['GET', 'POST'])
@login_required

def chatGPTFull_Topicname():
    global maxlistadmin
    Dbman = DB()
    
    if request.method == 'POST':

     try:
        edittype = request.args.get("edittype")
        topicname = request.args.get("topicname")
        username=current_user.email
        if (edittype=="add"):
            
                params1 = {"username1":username,"chatuser": 'user',"gptouttext": '',"keyword": '', "jiluzt": '0',"topicname":topicname}
                Dbman.insert('chatgpt_info', params_dic=params1)   
                Dbman.commit()
        elif(edittype=="del"):
    
                Dbman.delete(table_name='chatgpt_info', where="username1 = '%s'   and  jiluzt='0'  and   ( keyword IS   NULL  or length(keyword)<=0)  and topicname='%s'"  %(username,topicname))
                Dbman.commit()     
        elif(edittype=="modify"):
            
            oldtopicname = request.args.get("oldtopicname")
    
            params_dic={"topicname":topicname}
            Dbman.update( table_name='chatgpt_info', params_dic=params_dic, where="username1 = '%s'   and  jiluzt='0'  and   ( keyword IS   NULL  or length(keyword)<=0)  and topicname='%s'"  %(username,oldtopicname), update_date=True)
            Dbman.commit()     
     except Exception as e:
           print(('\t抱歉，ChatGPT负载过高,请稍后重试\t%s' % e))    
    if topicname==None:
        topicname=""
    return render_template('chatGPTFull.html',topicname=topicname)

@app.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        print(current_user.confirmed)
        return redirect(url_for('main12'))
    return render_template('auth/unconfirmed.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if 'chat_history' not in session:
        session['chat_history'] = []        
    else:
        print("item[1]:")
        total_length = sum(len(item[1]) for item in session['chat_history'])

        if (total_length>=4000):
            #request.set_cookie('chat_history', '')
            session['chat_history'] = []   
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('chatGPTFull')
            return redirect(next)
        flash('无效的邮件或密码.')
    return render_template('auth/login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username=form.email.data.lower()

        user = User(email=username,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认你的账户',
                   'auth/email/confirm', user=user, token=token)
        flash('已通过电子邮件向您发送确认电子邮件！') 
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)





def send_email(email,msg,reurl,user,token):# 发送验证邮件  

    print("发送邮件")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登录！')
    return redirect(url_for('login'))
@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main'))
    if current_user.confirm(token):
        db.session.commit()
        flash('您已确认您的帐户！谢谢！')
    else:
        flash('确认链接无效或已过期！')
    return redirect(url_for('main'))


@app.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认你的账户',
               'auth/email/confirm', user=current_user, token=token)
    flash('已通过电子邮件向您发送确认电子邮件！')
    return redirect(url_for('main'))



if __name__ == "__main__":

    app.run(
      host='127.0.0.1',
      port= 5000,

     )

