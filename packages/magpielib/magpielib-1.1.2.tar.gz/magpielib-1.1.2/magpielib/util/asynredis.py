import asyncio
from threading import Thread
from asyncio import iscoroutine
from redis.client import StrictRedis
from magpielib.util.log import get_logger
logger = get_logger("pcore")


def _start_loop(_loop):
    asyncio.set_event_loop(_loop)
    _loop.run_forever()


class AsyncRedisHandler:
    trans_loop = None
    bucket_map = {}

    def __init__(self, redis_host, redis_port, redis_password, redis_db):
        """保证一个进程只有一个trans_loop，而且这个loop 只干微事务同步这件事
        同时根据pcore 配置 初始化 bucket
        """
        if AsyncRedisHandler.trans_loop is None:
            # 初始化全局trans_loop 并启动线程跑起来
            trans_loop = asyncio.new_event_loop()
            Thread(target=_start_loop, args=(trans_loop,)).start()
            self.loop = trans_loop
            AsyncRedisHandler.trans_loop = trans_loop
        else:
            self.loop = AsyncRedisHandler.trans_loop
        # 缓存起来，这样就不用每次都去ping 了，保证一个进程有一个连接
        key = "%s%s%s%s" % (redis_host, redis_port, redis_password, redis_db)
        if key not in AsyncRedisHandler.bucket_map:
            # init bucket
            bucket = StrictRedis(host=redis_host, port=redis_port, password=redis_password,
                                 db=redis_db, decode_responses=True)
            ok = bucket.ping()
            if not ok:
                raise Exception("redis 配置有误，无法连接到redis服务器...")
            AsyncRedisHandler.bucket_map[key] = bucket
            self.bucket = bucket
        else:
            self.bucket = AsyncRedisHandler.bucket_map[key]

    def run_coro(self, coro):
        if not iscoroutine(coro):
            raise Exception("coro 不是一个协程方法。。。")
        asyncio.run_coroutine_threadsafe(coro, self.loop)
