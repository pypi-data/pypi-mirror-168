#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 1:58 下午
# @Author  : Meng Wang
# @Site    : 
# @File    : mysql_client.py
# @Software: PyCharm

import pymysql

class MysqlClient(object):

    def __init__(self, ip, port, username, password, db_name=""):
        self.connection = pymysql.connect(
            host=ip,
            user=username,
            passwd=password,
            db=db_name,
            port=int(port),
            charset='utf8',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )

    def query_by_sql(self, query_sql):
        cursor = self.connection.cursor()
        try:
            # 执行sql语句
            cursor.execute(query_sql)
            # 提交到数据库执行
            results = cursor.fetchall()
            return results
        except:
            # 如果发生错误则回滚
            self.connection.rollback()
        finally:
            # 关闭数据库连接
            self.connection.close()
