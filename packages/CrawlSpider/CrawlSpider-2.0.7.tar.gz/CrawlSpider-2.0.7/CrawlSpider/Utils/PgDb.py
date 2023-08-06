import time
import traceback
import psycopg
from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB


"""
usage:  https://www.psycopg.org/psycopg3/docs/basic/usage.html#module-usage
"""
class PgDb:
    """A lightweight wrapper around psycopg for easy to use
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接

    # example instance
    pg_db = PgDb(dbname='xx', user="postgres", host='127.0.0.1')
    """
    def __init__(self,
                 name='PgDb',
                 creator=psycopg,
                 maxusage=None,
                 dbname=None,
                 user=None,
                 host='127.0.0.1',
                 password=None,
                 isShare=False,
                 setsession=None,
                 failures=None,
                 ping=1,
                 closeable=False,
                 threadlocal=None,
                 maxconnections=20,
                 mincached=5,
                 maxcached=10,
                 maxshared=3,
                 *args,
                 **kwargs):
        """
        referer psycopg PersistentDB init
        :param creator:
        :param maxusage:threadlocal
        :param dbname:
        :param user:
        :param host:
        :param password:
        :param setsession:
        :param failures:
        :param ping:
        :param closeable:
        :param threadlocal:
        :param args:
        :param kwargs:
        """
        self.name = name
        self.creator = creator
        self.args = args
        if not isShare:
            kwargs.update(dict(
                maxusage=maxusage,
                dbname=dbname,
                user=user,
                host=host,
                password=password,
                setsession=setsession,
                failures=failures,
                ping=ping,
                closeable=closeable,
                threadlocal=threadlocal,
            ))
        else:
            kwargs.update(dict(
                maxusage=maxusage,
                dbname=dbname,
                user=user,
                host=host,
                password=password,
                setsession=setsession,
                failures=failures,
                ping=ping,
                maxconnections=maxconnections,
                mincached=mincached,
                maxcached=maxcached,
                maxshared=maxshared,
            ))
        self.kwargs = kwargs
        self.pool = PersistentDB(creator, *args, **kwargs) if not isShare else PooledDB(creator, *args, **kwargs)

    @staticmethod
    def getDict(description, rows):
        """
        use description and fetchResult to transfer list to dict
        :param description:
        :param rows:
        :return:
        """
        res = {}
        if rows:
            list_header = [row[0] for row in description]
            list_result = [[item for item in row] for row in rows]
            res = [dict(zip(list_header, row)) for row in list_result]
        return res

    def connection(self):
        """
        get a valid connection
        :return:
        """
        print(f"{self.name} connecting to db", flush=True)
        while 1:
            try:
                if not self.pool:
                    self.pool = PersistentDB(self.creator, *self.args, **self.kwargs)
                conn = self.pool.connection()
                return conn
            except Exception as e:
                time.sleep(0.5)
                print(f"connection: {e}")


    def fetchall(self, query):
        """Returns a List[dict] for the given query and parameters.
        param query
        return List[dict]
        ss
        # example fetch all
        items = pg_db.fetchall('select * from test')
        print(items)
        """
        conn = self.connection()
        with conn.cursor() as cur:
            try:
                cur.execute(query)
                res = self.getDict(cur.description, cur.fetchall())
            except Exception as e:
                print(f"{self.name}:  -- {traceback.format_exc()}")
                conn._ping_check()
                cur.execute(query)
                res = self.getDict(cur.description, cur.fetchall())
            return res

    def fetchone(self, query):
        """Returns a row dict for the given query and parameters.
        :param query: sql query
        :return dict
        # example fetchone
        itemList = pg_db.fetchall("select * from test")
        print(len(itemList))
        """
        conn = self.connection()
        with conn.cursor() as cur:
            try:
                cur.execute(query)
                item = cur.fetchone()

                rows = item and [item] or []
                res = self.getDict(cur.description, rows) or []
                if res:
                    res = res[0]
            except Exception as e:
                conn._ping_check()
                print(f"{self.name}:  -- {traceback.format_exc()}")
                cur.execute(query)
                item = cur.fetchone()
                rows = item and [item] or []
                res = self.getDict(cur.description, rows) or []
                if res:
                    res = res[0]
            finally:
                cur.close()
                conn.close()
            return res


    def fetchmany(self, query, size=1000):
        """Returns many rows dict for the given query and parameters.
        :param query
        :param size default 1000
        :return List[dict]
        # example fetchmany
        for itemList in pg_db.fetchmany('select * from test', size=3):
            print(itemList)
        """
        conn = self.connection()
        res = []
        with conn.cursor() as cur:
            try:
                cur.execute(query)

                while 1:
                    itemList = cur.fetchmany(size=size)
                    res = self.getDict(cur.description, itemList)
                    if len(res) < size:
                        break

                    yield res

            except Exception as e:
                print(f"{self.name}:  -- {traceback.format_exc()}")
                conn._ping_check()
                self.fetchmany(query=query, size=size)
            finally:
                cur.close()
                conn.close()
            yield res

    def execute(self, query, *parameters, **kwparameters):
        """Executes the given query"""
        conn = self.connection()
        with conn.cursor() as cur:
            try:
                ret = cur.execute(query, kwparameters or parameters)
                # ret = ret.statusmessage
                ret = ret and hasattr(ret, 'statusmessage') and ret.statusmessage or None
                conn.commit()
            except Exception as e:
                print(f"{self.name}:  -- {traceback.format_exc()}")
                conn.rollback()
                ret = e
            finally:
                cur.close()
                conn.close()
        return ret


    def executeMany(self, query, *parameters, **kwparameters):
        """Executes the given query, batch execute
        """
        conn = self.connection()
        with conn.cursor() as cur:
            try:
                ret = cur.executemany(query, kwparameters or parameters)
                ret = ret and hasattr(ret, 'statusmessage') and ret.statusmessage or None
                conn.commit()
            except Exception as e:
                print(f"{self.name}:  -- {traceback.format_exc()}")
                conn.rollback()
                ret = e
            finally:
                cur.close()
                conn.close()
        return ret

    def table_has(self, table_name, conditions:dict=None, condition=None):
        """
        judge record that  is or not in table
        :param table_name:
        :param conditions: select condition:
        :param condition: select condition:
        :return:

        example:
        # judge record is or not in table
        # print(pg_db.table_has('test', {
        #     'name': 'search'
        # }))
        """
        if not condition:
            if not isinstance(conditions, dict):
                raise TypeError('conditions must be dict')
            condition, _ = self.flat(conditions, condition=True, sep=' and ')

        query = f'SELECT * FROM {table_name} WHERE {condition}'
        res = self.fetchone(query)
        if res and len(res):
            return True
        return False

    def table_insert(self, table_name, item, ignore_duplicated=True, on=''):
        """
        insert data(dict) to table
        :param table_name:
        :param item:
        :param ignore_duplicated:
        :param on:
        :return:

        # example insert one
        res = pg_db.table_insert('test', {
            'id': 11,
            'name': 'search',
        })
        print(res)
        """
        fields = list(item.keys())
        values = list(item.values())
        fieldstr = ','.join(fields)
        valstr = ','.join(['%s'] * len(item))
        sql = f'INSERT INTO {table_name} ({fieldstr}) VALUES({valstr}) {on}'
        ret = self.execute(sql, *values)

        if isinstance(ret, Exception):
            ret = ret.args[-1]
            if ignore_duplicated and '已经存在' in ret:
                # just skip duplicated item
                ret = 'INSERT 0 0'
            else:
                for i in range(len(fields)):
                    vs = str(values[i])
                    if len(vs) > 50:
                        print(fields[i], ' : ', len(vs), type(values[i]))
                    else:
                        print(fields[i], ' : ', vs, type(values[i]))
        print(f"{self.name}: {ret}")
        return ret

    def table_insertMany(self, table_name, itemList, on=''):
        """
        insert many data==> List(dict) to table
        :param table_name:
        :param itemList:
        :param on : on conflict(id) do nothing;
        :return:

        # example insert many
        res = pg_db.table_insertMany('test', [
            {
                'id': 11,
                'name': 'jjj',

            },
            {
                'id': 12,
                'name': 'jjj',

            },
        ])
        print(res)
        """
        if not itemList:
            raise ValueError("itemList can't None")
        item:dict = itemList[0]
        fields = item.keys()
        fieldstr = ','.join(fields)
        valstr = ','.join(['%s'] * len(fields))
        sql = f'INSERT INTO {table_name} ({fieldstr}) VALUES({valstr}) {on}'

        ret = self.executeMany(sql, *[tuple(item.values()) for item in itemList])


        if isinstance(ret, Exception):
            ret = ret.args[-1]

        print(f"{self.name}: {ret}")
        return ret

    @staticmethod
    def flat(updates, condition=False, sep=','):
        upsets = []
        values = []
        for k, v in updates.items():
            s = '%s=%%s' % k
            if condition:
                s = "%s='%s'" % (k, v)
                if isinstance(v, tuple):
                    s = f"{k} in {v}"
                elif isinstance(v, (int, float)):
                    s = f"{k} = {v}"
                elif 'null' in v.lower():
                    s = f"{k} is {v}"

            upsets.append(s)
            values.append(v)
        upsets = sep.join(upsets)

        return upsets, values

    def table_update(self, table_name, updates:dict, conditions:dict= None, condition=None):
        """
        according to condtions(dict) to update some field (updates) ==> dict
        :param table_name:
        :param updates:
        :param conditions:
        :param condition:
        :return:

        # example update:

        res = pg_db.table_update('test', {
            'name': 'hello'
        },condition='id between 1 and 4')
        print(res)
        """

        upsets, values = self.flat(updates)
        if not condition:
            if not isinstance(conditions, dict):
                raise TypeError('conditions must be dict')
            condition, _ = self.flat(conditions, condition=True, sep=' and ')
        sql = f'UPDATE {table_name} SET {upsets} WHERE {condition}'
        ret = self.execute(sql, *(values))
        if isinstance(ret, Exception):
            ret = ret.args[-1]

        print(f"{self.name}: {ret}")
        return ret
