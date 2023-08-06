
import traceback
import psycopg
from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB


class PgDb:
    """A lightweight wrapper around psycopg for easy to use
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接
    """
    def __init__(self,
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
        if not self.pool:
            self.pool = PersistentDB(self.creator, *self.args, **self.kwargs)
        return self.pool.connection()

    def fetchall(self, query):
        """Returns a List[dict] for the given query and parameters."""
        conn = self.connection()
        with conn.cursor() as cur:
            try:
                cur.execute(query)
                res = self.getDict(cur.description, cur.fetchall())
            except Exception as e:
                conn._ping_check()
                cur.execute(query)
                res = self.getDict(cur.description, cur.fetchall())
            return res

    def fetchone(self, query):
        """Returns a row dict for the given query and parameters."""
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
        """Returns a row dict for the given query and parameters."""
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
                cur.execute(query, kwparameters or parameters)
                conn.commit()
            except Exception as e:
                conn.rollback()
                return e.args[-1]
            finally:
                cur.close()
                conn.close()



    def executeMany(self, query, *parameters, **kwparameters):
        """Executes the given query, batch execute"""
        conn = self.connection()
        with conn.cursor() as cur:
            try:
                cur.executemany(query, kwparameters or parameters)
                conn.commit()
            except Exception as e:
                conn.rollback()
                return e.args[-1]
            finally:
                cur.close()
                conn.close()


    def table_has(self, table_name, conditions):
        """
        judge record that  is or not in table
        :param table_name:
        :param field:
        :param value:
        :return:
        """
        condition, _ = self.flat(conditions, condition=True, sep=' and ')
        query = f'SELECT * FROM {table_name} WHERE {condition}'
        res = self.fetchone(query)
        if res and len(res):
            return True
        return False

    def table_insert(self, table_name, item, ignore_duplicated=True):
        """
        insert data(dict) to table
        :param table_name:
        :param item:
        :param ignore_duplicated:
        :return:
        """
        fields = list(item.keys())
        values = list(item.values())
        fieldstr = ','.join(fields)
        valstr = ','.join(['%s'] * len(item))
        sql = 'INSERT INTO %s (%s) VALUES(%s)' % (table_name, fieldstr, valstr)
        try:
            last_id = self.execute(sql, *values)
            return last_id
        except Exception as e:
            if ignore_duplicated and e.args[0] == 1062:
                # just skip duplicated item
                return 0
            traceback.print_exc()
            print('sql:', sql)

            for i in range(len(fields)):
                vs = str(values[i])
                if len(vs) > 300:
                    print(fields[i], ' : ', len(vs), type(values[i]))
                else:
                    print(fields[i], ' : ', vs, type(values[i]))
            return e

    def table_insertMany(self, table_name, itemList):
        """
        insert many data==> List(dict) to table
        :param table_name:
        :param itemList:
        :return:
        """
        if not itemList:
            raise ValueError("itemList can't None")
        item:dict = itemList[0]
        ks = item.keys()
        fieldstr = ','.join(ks)
        valstr = ','.join(['%s'] * len(ks))
        sql = 'INSERT INTO %s (%s) VALUES(%s)' % (table_name, fieldstr, valstr)
        try:
            last_id = self.executeMany(sql, *[tuple(item.values()) for item in itemList])
            return last_id
        except Exception as e:
            traceback.print_exc()
            print('sql:', sql)
            return e

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
                elif 'null' in v.lower():
                    s = f"{k} is {v}"

            upsets.append(s)
            values.append(v)
        upsets = sep.join(upsets)

        return upsets, values

    def table_update(self, table_name, updates,
                     conditions):
        """
        according to condtions(dict) to update some field (updates) ==> dict
        :param table_name:
        :param updates:
        :param conditions:
        :return:
        """

        upsets, values = self.flat(updates)
        condition, _ = self.flat(conditions, condition=True, sep=' and ')
        sql = 'UPDATE %s SET %s WHERE %s' % (
            table_name,
            upsets,
            condition
        )
        self.execute(sql, *(values))


if __name__ == '__main__':
    pg_db = PgDb(dbname='spider', user="postgres", host='127.0.0.1', isShare=True)
    # example fetchone
    pg_db.fetchone('select * from test')
    # example fetchmany
    for itemList in pg_db.fetchmany('select * from test', size=3):
        print(itemList)



    # example insert one
    # res = pg_db.table_insert('plat_info', {
    #     'platform': 'wanfang',
    #     'view_desc': 'search',
    #     'view_url': 'https://s.wanfangdata.com.cn/thesis?q=专业%3A"一般力学与力学基础"'
    # })
    # print(res)
    # example insert many
    # res = pg_db.table_insertMany('plat_info', [
    #     {
    #         'platform': 'publons',
    #         'view_desc': 'detail',
    #         'view_url': 'https://publons.com/researcher/A-1001-2010/'
    #     },
    #     {
    #         'platform': 'publons',
    #         'view_desc': 'stats',
    #         'view_url': 'https://publons.com/api/stats/individual/2878410/'
    #     },
    #     {
    #         'platform': 'publons',
    #         'view_desc': 'profile_summary',
    #         'view_url': 'https://publons.com/api/profile/summary/2878410/'
    #     },
    #     {
    #         'platform': 'publons',
    #         'view_desc': 'profile_publication',
    #         'view_url': 'https://publons.com/api/profile/publication/2878410/?order_by=citations&page=1&per_page=5'
    #     }
    # ])
    # print(res)

    # example update
    # res = pg_db.table_update('wf_search_result', {
    #     'kw': '作者单位:电子科技大学'
    # },{
    #     'kw': '作者单位:("电子科技大学")'
    # })
    # print(res)

    # judge record is or not in table
    # print(pg_db.table_has('plat_info', {
    #     'platform': 'wanfang',
    #     'view_desc': 'detail'
    # }))



