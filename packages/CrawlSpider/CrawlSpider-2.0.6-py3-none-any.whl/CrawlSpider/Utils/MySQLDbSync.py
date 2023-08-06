# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/4/23 0:08
# __fileName__ : wx_kam_robot mysqlDbSync.py
# __devIDE__ : PyCharm

import pymysql
from dbutils.pooled_db import PooledDB
from contextlib import contextmanager
import traceback
divLen = 5

class MySQLDb:
    def __init__(self, connect_params):
        self.connect_params:dict = connect_params
        self.instanced()

    def instanced(self):
        # , ping=2
        self.poolDB = PooledDB(pymysql, mincached=5, maxcached=20, maxconnections=20, blocking=True, **self.connect_params)

    def get_conn(self):
        if self.poolDB is None:
            self.instanced()
        while 1:
            try:
                return self.poolDB.connection()
            except Exception:
                print(traceback)

    @contextmanager
    def selectAll(self, sql):
        conn_python = self.get_conn()
        cursor_python = conn_python.cursor(pymysql.cursors.DictCursor)
        try:
            cursor_python.execute(sql)
            result = cursor_python.fetchall()

            yield result
        except Exception as e:
            print(traceback.format_exc())
            yield None
        finally:
            cursor_python.close()
            conn_python.close()

    @contextmanager
    def getCount(self, sql):
        if ('count' not in sql.lower()):
            yield 'NoCount'
        else:
            conn_python = self.get_conn()
            cursor_python = conn_python.cursor(pymysql.cursors.DictCursor)
            # sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
            try:
                cursor_python.execute(sql)
                result = cursor_python.fetchall()
                # print(result[0])
                yield result
            except Exception as e:
                print(traceback.format_exc())
                yield None
            finally:
                cursor_python.close()
                conn_python.close()

    @contextmanager
    def insertMany(self, sql, params):
        conn_python = self.get_conn()
        cursor_python = conn_python.cursor()
        yield sql
        try:
            cursor_python.executemany(sql, params)
            conn_python.commit()
        except Exception as e:
            print(f'总共插入: {len(params)}条数据')
            conn_python.rollback()
            print(traceback.format_exc())
            write_flag = 0
            length = len(params)

            for i in range(0, length, divLen):
                res = params[i:(i + divLen)]
                try:
                    cursor_python.executemany(sql, res)
                    conn_python.commit()
                except Exception as e:

                    conn_python.rollback()

                    for param in res:
                        try:
                            cursor_python.execute(sql, param)
                            conn_python.commit()
                        except Exception as e:
                            conn_python.rollback()
                            print("param:", param)
                            write_flag += 1
        finally:
            cursor_python.close()
            conn_python.close()

    @contextmanager
    def insertOneByOne(self, sql, params):
        conn_python = self.get_conn()
        cursor_python = conn_python.cursor()
        yield sql
        for param in params:
            try:
                # print(params[0])
                cursor_python.execute(sql, param)
                conn_python.commit()
            except Exception as e:
                print(traceback.format_exc())
                conn_python.rollback()
        else:
            cursor_python.close()
            conn_python.close()

    @contextmanager
    def delete(self, sql, params=None):
        conn_python = self.get_conn()
        cursor_python = conn_python.cursor()
        yield sql
        try:
            if (params):
                cursor_python.execute(sql, params)
            else:
                cursor_python.execute(sql)
            conn_python.commit()
        except Exception as e:
            print(e)
            conn_python.rollback()
        finally:
            cursor_python.close()
            conn_python.close()

    @contextmanager
    def update(self, sql, params=None):
        conn_python = self.get_conn()
        cursor_python = conn_python.cursor()
        yield sql
        try:
            if (params):
                cursor_python.execute(sql, params)
            else:
                cursor_python.execute(sql)
            conn_python.commit()
        except Exception as e:
            print(e)
            conn_python.rollback()
        finally:
            cursor_python.close()
            conn_python.close()

    def table_select(self, table, db=None, condition=None):
        # 'select * from wechat_conf where status=0  and id<10000'
        db = db or self.connect_params.get('db')
        sql = f"select * from {db}.{table} {condition}"
        print(sql)
        with self.selectAll(sql) as rows:
            return rows

    def table_insert(self, table, item, db=None):
        """
        :param item: kwargs={} 字典形式
        :return:
        """
        db = db or self.connect_params.get('db')
        keys = ','.join(item.keys())
        values = ','.join(['%s'] * len(item))
        sql = f'INSERT INTO {db}.{table}({keys}) VALUES ({values})'
        params = [tuple(item.values())]  # 必须是元祖形式
        with self.insertMany(sql, params=params) as fmt_sql:
            print(fmt_sql)
        print('插入完毕: %s' % str(len(params)), end='')

    def table_insertMany(self,table,  itemList:list, db=None):
        """
        :param kwargs: kwargs=[{},...]  嵌套字典形式
        :return:
        """
        db = db or self.connect_params.get('db')
        item = itemList[0]
        keys = ','.join(item.keys())
        values = ','.join(['%s'] * len(item))
        sql = f'INSERT INTO {db}.{table}({keys}) VALUES ({values})'
        params = []
        for item in itemList:
            params.append(tuple(item.values()))  # 子元素必须是元组形式
        with self.insertMany(sql, params=params) as fmt_sql:
            print(fmt_sql)
        print('插入完毕: %s' % str(len(params)), end='')

