# coding=utf-8

import pymysql.cursors
import string
import datetime
import sys
import dbconfig as dbconfig

class DB(object):
    def __init__(self, conf=None):
        self.conn = self.__getConn(conf)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute('SET NAMES utf8')
        self.cursor.execute("SET CHARACTER SET utf8")
        self.cursor.execute("SET character_set_connection=utf8")

    def __del__(self):
        self.cursor.close()
        self.conn.close()
    
    def __getConn(self, conf=None):

    
        return pymysql.connect(
            host=dbconfig.host,
            port=dbconfig.port,
            user=dbconfig.user,
            password=dbconfig.password,
            db=dbconfig.db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def execute(self, sql, param=None):
        """Execute SQL statement"""
        rowcount = 0
        try:
            if param is None:
                rowcount = self.cursor.execute(sql)
            else:
                rowcount = self.cursor.execute(sql, param)
            return rowcount
        except Exception as e:
            print('--------------Error--------')
            print(e)
            return 0
    
    def queryOne(self, sql, param=None):
        """Get one record"""
        rowcount = self.cursor.execute(sql, param)
        if rowcount > 0:
            res = self.cursor.fetchone()
        else:
            res = None
    
        return res
    
    def queryAll(self, sql, param=None):
        """Get all records"""
        rowcount = self.cursor.execute(sql, param)
        if rowcount > 0:
            res = self.cursor.fetchall()
        else:
            res = []
        return res
    
    def begin(self):
        """Start transaction"""
        self.cursor.execute("SET AUTOCOMMIT = 0")
    
    def end(self):
        """End transaction"""
        self.cursor.execute("SET AUTOCOMMIT = 1")
    
    def commit(self):
        """Commit transaction"""
        self.conn.commit()
    
    def rollback(self):
        """Roll back transaction"""
        self.conn.rollback()
    
    def select(self, table_name, columns='*', where=None):
        if isinstance(columns, str):
            columns_str = str(columns)
        elif isinstance(columns, (list, tuple)):
            if not columns:
                columns_str = '*'
            else:
                columns_str = ','.join(str(c) for c in columns)
    
        if isinstance(where, dict) and where:
            items = list(where.items())
            if len(items) == 1 and isinstance(items[0][0], (list, tuple)) and items[0][0]:
                self.execute("SELECT %s FROM %s WHERE %s in (%s)" % (
                columns_str, table_name, items[0], ','.join(str(e) for e in items[1])))
                sel2qq="SELECT %s FROM %s WHERE %s in (%s)" % (columns_str, table_name, items[0], ','.join(str(e) for e in items[1]))
                print(sel2qq) 
            else:
                sql, values = self.sql_and_values_for_dict(table_name, columns, where)
                print(sql) 

                self.execute(sql, values)
        elif isinstance(where, str) and where:
            self.execute("SELECT %s FROM %s WHERE %s" % (columns_str, table_name, where))
            sel2qq="SELECT %s FROM %s WHERE %s" % (columns_str, table_name, where)
            print(sel2qq) 
        else:
            self.execute("SELECT %s FROM %s " % (columns_str, table_name))
    
    def selectOne(self, table_name, columns='*', where=None):
        self.select(table_name, columns, where)
        return self.cursor.fetchone()
    
    def selectAll(self, table_name, columns='*', where=None):
        print("取出的结果11：")    

        print(where)
        self.select(table_name, columns, where)
        return self.cursor.fetchall()


    def insert(self, table_name, params_dic):
        """Insert records"""
        if not isinstance(params_dic, dict):
            print('The input parameter is not a dict.')
            return False
    
        if len(params_dic) == 0:
            print('The input dict is empty.')
            return False
    
        try:
            keys = ','.join(list(params_dic.keys()))
            values = ','.join(['%s'] * len(list(params_dic.keys())))
            sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, keys, values)
            rowcount = self.cursor.execute(sql, tuple(params_dic.values()))
            if rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print('--------------Error--------')
            print(e)
            return False
        # update

    def update(self, table_name, params_dic, where=None, update_date=True):
        #if update_date:
            #params_dic.update({'updated_at': type(self).get_datetime_string()})
        edit_sql = ",".join([("%s" % (str(x)) + "=%s") for x in list(params_dic.keys())])
        values = [str(x) for x in list(params_dic.values())]
        where_sql = ''

        if where:
            if isinstance(where, str):
                where_sql = str(where)
            elif isinstance(where, dict):
                where_sql = " AND ".join([("%s" % (str(x)) + "=%s") for x in list(where.keys())])
                where_values = [str(x) for x in list(where.values())]
                values = values + where_values
            sql = "UPDATE %s SET %s WHERE %s" % (table_name, edit_sql, where_sql)
        else:
            sql = "UPDATE %s SET %s " % (table_name, edit_sql)

        return self.execute(sql, values)

    # delete
    def delete(self, table_name, where=None):
        where_sql = ''
        if where:
            if isinstance(where, str):
                where_sql = where
            elif isinstance(where, dict):
                where_sql = " AND ".join(["%s='%s'" % (str(x[0]), str(x[1])) for x in list(where.items())])
            sql_prefix = "DELETE FROM %s WHERE %s "
            sql = sql_prefix % (table_name, where_sql)
        else:
            sql_prefix = "DELETE FROM %s "
            sql = sql_prefix % (table_name)

        return self.execute(sql)

    def get_inserted_id(self):
        """
        获取当前连接最后一次插入操作[自增长]生成的id,如果没有则为０
        """
        result = self.queryAll("SELECT @@IDENTITY AS id")
        if result:
            return result[0].get('id')
        return 0
        #################### classmethods

    @classmethod
    def get_datetime_string(cls):
        return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def generate_code(cls):
        import time
        import random
        return '%x%x' % (int(time.time()), random.randint(1, 0x0ffff))

    @classmethod
    def generate_id(cls):
        return "n%s" % cls.generate_code()