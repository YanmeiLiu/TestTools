#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain

import pymysql as mysql
import os
import configparser

from log.log import write_log

project_dir = os.path.dirname(os.path.abspath(__file__))

logger = write_log(__name__)


# mysql类，传入数据库后选择操作方法

class Mysql(object):
    def __init__(self, dbname):
        self.dbname = dbname

    def get_db_ini(self):
        cf = configparser.RawConfigParser()
        cf.read(project_dir + '/db.ini', encoding='utf-8')
        host, user, password, dbname, charset = [x[1] for x in cf.items(self.dbname)]
        return host, user, password, dbname, charset

    def connect(self):
        host, user, password, db, charset = self.get_db_ini()
        try:
            conn = mysql.connect(host=host, user=user, passwd=password, db=db, charset=charset)
            return conn
        except Exception as e:
            logger.warning(e)
            return '数据库连接失败'

    def select(self, sql, fetchone=False):
        conn = self.connect()
        if conn == '数据库连接失败':
            return conn

        cur = conn.cursor()
        try:
            cur.execute(sql)
            # print(type(cur))

            if cur.rowcount == 0:
                return
            if fetchone:
                res = cur.fetchone()
                return res
            else:
                res = cur.fetchall()
                # res = list(chain.from_iterable(res))
                return res

        except Exception as e:
            logger.warning(e)
            return

        finally:
            conn.close()

    def insert(self, sql):
        conn = self.connect()
        if conn == '数据库连接失败':
            return conn

        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            logger.warning(e)
            return False
        finally:
            conn.close()

    def update(self, sql):
        conn = self.connect()
        if conn == '数据库连接失败':
            return conn

        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            return '更新成功'
        except Exception as e:
            conn.rollback()
            logger.warning(e)
            return '更新失败'
        finally:
            conn.close()

    def delete(self, sql):
        conn = self.connect()
        if conn == '数据库连接失败':
            return conn

        cur = conn.cursor()
        try:
            cur.execute(sql)
            conn.commit()
            return '删除成功'
        except Exception as e:
            conn.rollback()
            logger.warning(e)
            return '删除失败'
        finally:
            conn.close()


if __name__ == '__main__':
    Mysql('test_vip').connect()
