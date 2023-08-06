
import traceback
import aiomysql
import pymysql




class MySQLDb:
    """A lightweight wrapper around aiomysql.Pool for easy to use
    """
    def __init__(self, host, user, password,
                 db=None,
                 loop=None, sanic=None,
                 minsize=3, maxsize=5,
                 return_dict=True,
                 pool_recycle=7*3600,
                 autocommit=True,
                 charset = "utf8mb4", **kwargs):
        '''
        kwargs: all parameters that aiomysql.connect() accept.
        '''
        self.db_args = {
            'host': host,
            'db': db,
            'user': user,
            'password': password,
            'minsize': minsize,
            'maxsize': maxsize,
            'charset': charset,
            'loop': loop,
            'autocommit': autocommit,
            'pool_recycle': pool_recycle,
        }
        self.sanic = sanic
        # if sanic:
        #     sanic.db = self
        if return_dict:
            self.db_args['cursorclass']=aiomysql.cursors.DictCursor
        if kwargs:
            self.db_args.update(kwargs)
        self.pool = None

    async def init_pool(self):
        if self.sanic:
            self.db_args['loop'] = self.sanic.loop
        self.pool = await aiomysql.create_pool(**self.db_args)

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

    async def fetchall(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters."""
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters or None)
                    ret = await cur.fetchall()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters or None)
                    ret = await cur.fetchall()
                return ret

    async def fetchone(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query.
        """
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchone()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters)
                    ret = await cur.fetchone()
                return ret

    async def execute(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters or None)

                except Exception:
                    # https://github.com/aio-libs/aiomysql/issues/340
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters or None)
                return cur.lastrowid

    # executemany
    async def executeMany(self, query, items):
        """Executes the given query, returning the lastrowid from the query."""
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.executemany(query, items)
                except Exception:
                    # https://github.com/aio-libs/aiomysql/issues/340
                    await conn.ping()
                    await cur.executemany(query, items)
                return cur.lastrowid
    # high level interface
    async def table_has(self, table_name, conditions):
        """
        judge record that  is or not in table
        :param table_name: table to fetching
        :param conditions: fetch condtions
        :return:
        """
        condition, _ = self.flat(conditions, condition=True, sep=' and ')
        query = f'SELECT * FROM {table_name} WHERE {condition}'
        res = await self.fetchone(query)
        if res and len(res):
            return True
        return False

    async def table_insert(self, table_name, item, ignore_duplicated=True):
        '''item is a dict : key is mysql table field'''
        fields = list(item.keys())
        values = list(item.values())
        fieldstr = ','.join(fields)
        valstr = ','.join(['%s'] * len(item))
        sql = 'INSERT INTO %s (%s) VALUES(%s)' % (table_name, fieldstr, valstr)
        try:
            last_id = await self.execute(sql, *values)
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

    async def table_insertMany(self, table_name, items):
        '''item is a dict : key is mysql table field'''
        item = items[0]
        fields = list(item.keys())
        values = list(item.values())
        fieldstr = ','.join(fields)
        valstr = ','.join(['%s'] * len(item))
        sql = 'INSERT INTO %s (%s) VALUES(%s)' % (table_name, fieldstr, valstr)
        try:
            data = []
            for item in items:
                data.append(tuple(item.values()))
            last_id = await self.executeMany(sql, data)
            return last_id
        except Exception as e:
            traceback.print_exc()
            print('sql:', sql)

            for i in range(len(fields)):
                vs = str(values[i])
                if len(vs) > 300:
                    print(fields[i], ' : ', len(vs), type(values[i]))
                else:
                    print(fields[i], ' : ', vs, type(values[i]))
            return e


    async def table_update(self, table_name, updates,
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
        await self.execute(sql, *values)
