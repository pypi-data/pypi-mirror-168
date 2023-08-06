import uuid
import math
import time
import redis

class RedisDB:

    def __init__(self, config=None, lock_name=None):
        """
        :param config: {"host":"",
                        "port": 0,
                        "db": 0,
                        "password": "",
                        "encoding": "",
                        "decode_responses": False,
                        "max_connections": 1,
                        "target_max_memory": 1024
                        }
        """
        self.config = config
        pool = redis.ConnectionPool(**self.config)
        self.connection_pool = pool
        self.lock_name = lock_name or 'spider'

    def getClient(self):
        client = redis.Redis(connection_pool=self.connection_pool)
        return client

    def acquire_lock_with_timeout(self, conn, acquire_timeout=3, lock_timeout=2):
        """
        基于 Redis 实现的分布式锁
        :param conn: Redis 连接
        :param lock_name: 锁的名称
        :param acquire_timeout: 获取锁的超时时间，默认 3 秒
        :param lock_timeout: 锁的超时时间，默认 2 秒
        :return:
        """

        identifier = str(uuid.uuid4())
        lockname = f'lock:{self.lock_name}'
        lock_timeout = int(math.ceil(lock_timeout))

        end = time.time() + acquire_timeout

        while time.time() < end:
            # 如果不存在这个锁则加锁并设置过期时间，避免死锁
            if conn.set(lockname, identifier, ex=lock_timeout, nx=True):
                return identifier

            time.sleep(0.001)

        return False


    def release_lock(self, conn, identifier):
        """
        释放锁

        :param conn: Redis 连接
        :param lockname: 锁的名称
        :param identifier: 锁的标识
        :return:
        """
        unlock_script = """
        if redis.call("get",KEYS[1]) == ARGV[1] then
            return redis.call("del",KEYS[1])
        else
            return 0
        end
        """
        lockname = f'lock:{self.lock_name}'
        unlock = conn.register_script(unlock_script)
        result = unlock(keys=[lockname], args=[identifier])
        if result:
            return True
        else:
            return False

    def sadd(self, setName, *values):
        client = self.getClient()
        return client.sadd(setName, *values)


    def sismember(self, setName, value):
        client = self.getClient()
        return client.sismember(setName, value)

    def spop(self, setName):
        client = self.getClient()
        identifier = self.acquire_lock_with_timeout(client)
        value = 0
        if identifier:
            value = client.spop(setName)
            if not value:
                value = 1
            self.release_lock(client, identifier)

        return value













