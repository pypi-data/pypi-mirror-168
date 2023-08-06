# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2019/11/13 17:26
# __fileName__ : Python_Study SQLibs.py
# __devIDE__ : PyCharm
import pymysql
from dbutils.pooled_db import PooledDB
from contextlib import contextmanager
import traceback
from math import floor

class SQLib:
    def __init__(self, connect_params):
        self.connect_params = connect_params
        self.instanced()

    def instanced(self):
        # , ping=2
        self.poolDB = PooledDB(pymysql, mincached=10, maxcached=20, maxconnections=50, blocking=True, **self.connect_params)

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
            for param in params:
                print(param)
            conn_python = self.get_conn()
            cursor_python = conn_python.cursor()
            print(traceback.format_exc())
            print(sql)
            write_flag = 0
            length = len(params)

            if (length > 1000):
                count = floor(length / 1000) + 1
                try:
                    for i in range(count):
                        res = params[i * 1000:(i + 1) * 1000]
                        cursor_python.executemany(sql, res)
                        conn_python.commit()
                except Exception as e:
                    print(e)
            else:
                for param in params:
                    try:
                        cursor_python.execute(sql, param)
                        conn_python.commit()
                    except Exception as e:
                        write_flag += 1
                        print(e)
                        print(f"当前报错param:{param}")
                        conn_python.rollback()
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
                print(e)
                print(param)
                print(sql)
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


