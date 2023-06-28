# chatGPT-web-cn
中文版chatGPT，中国国内可以使用的chatGPT web版支持开发者部署服务给自己的用户使用。
采用python+flask+mysql开发。


# 项目名：仿真版chatGPT

## 简介

仿真版chatGPT是一个用openai接口实现的，基于Python+Flask框架+Mysql开发的大模型对话系统，支持话题的增删改查，支持连续对话，支持复制，并且提供友好的用户界面。用户需要进行简单的注册，才能开始使用。

chatGPT国内web版可用简单部署在服务器上就可以开放给用户使用。



![image](https://picgo-1305429599.cos.ap-guangzhou.myqcloud.com/picgo/image-20230429162313381.png){width="50%" height="50%"}

## 功能

- 用户注册和登录
- 发布和浏览chatGPT聊天记录，可永久记住
- 支持话题的增删改查
- 支持复制内容
- 支持互动式对话，提供优秀的chatGTP仿真交互界面
- 是办公干事必备利器


## 安装和使用

1. 克隆项目

```bash
git clone https://github.com/pythonmanGo/chatGPT-web-cn.git
```

ps1：本程序采用的python版本为python3.79

ps2：如果发现有图标文件缺失，请解压根目录下的fontawesome-free-6.4.0-web.zip文件,覆盖原来static/ontawesome-free-6.4.0-web目录即可。

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 导入数据库

```bash
1）安装mysql数据库
2）数据库在根目录下的database目录下的txt文件database.txt，导入mysql数据库中。
```

4. 配置openai云函数


    申请OPENAI的APIkey。
请参考 https://github.com/Ice-Hazymoon/openai-scf-proxy
      进行openai云函数配置 


5. 修改配置文件

```bash
修改根目录下配置文件robot.env，以下几项必须修改：
String_list =sk-xxxxx                          #openai key  可以放入更多的key，这样速度更快一些，用户之间不冲突。
YunHanshu=https://xxxxxx/                                                        #云函数地址
MYSQLURI=mysql+pymysql://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名         #mysqlURI地址
HOST=数据库地址
USER=数据库用户名
PORT=3306
PASSWORD=数据库密码
DBNAME=数据库名
```

6. 启动项目

```bash
python chatGPTFull.py
```



7. 访问项目

在浏览器中输入：http://localhost:5000

## 注意事项

该项目为仿真版chatGPT，仅供学习和研究使用，请勿在公共场合使用相关话题和内容。如有任何问题和建议，或者有进一步需求，欢迎联系开发者。有问题可以加入咨询群了解：
服务器资源和token有限，如需拿体验环境，也请加微信群沟通。



<img src="[https://picgo-1305429599.cos.ap-guangzhou.myqcloud.com/picgo/image-20230429162313381.png" alt="" style="zoom:50%;" />
## TODO List

1. 代码的简化&界面优化。（欢迎开发者加入，提供指导。）
2. 多模型支持。
3. 图片模型接入。
4. 个性化话题定制。
5. 自动识别话题并进行prompt联想，进一步提升易用性。

