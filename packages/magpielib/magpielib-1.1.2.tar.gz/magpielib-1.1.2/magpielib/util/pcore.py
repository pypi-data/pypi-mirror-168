import asyncio
import json
from threading import Thread
from asyncio import iscoroutinefunction
from redis.client import StrictRedis


def _start_loop(_loop):
    asyncio.set_event_loop(_loop)
    _loop.run_forever()


class SyncTransInfo:
    """为微事务同步类，参数校验已经在reqhandler中写了，这里直接取值
    从不同语言框架层面来说：要想微事务同步，必须符合这一标准。
    """
    def __init__(self, sync_trans):
        self.sid = sync_trans.get('sid')
        self.tid = sync_trans.get('tid')
        self.redis_host = sync_trans.get('redis').get('host')
        self.redis_port = sync_trans.get('redis').get('port')
        self.redis_password = sync_trans.get('redis').get('password')
        self.redis_db = sync_trans.get('redis').get('redis_db')


class SyncTransHandler:
    trans_loop = None

    def __init__(self, st_info: SyncTransInfo):
        """保证一个进程只有一个trans_loop，而且这个loop 只干微事务同步这件事
        同时根据pcore 配置 初始化 bucket
        """
        if st_info is None or st_info.tid is None or st_info.sid is None \
                or st_info.redis_db is None or st_info.redis_host is None \
                or st_info.redis_password is None:
            raise Exception("st_info 不合法，没有经过前端框架层校验")
        if SyncTransHandler.trans_loop is None:
            # 初始化全局trans_loop 并启动线程跑起来
            trans_loop = asyncio.new_event_loop()
            Thread(target=_start_loop, args=(trans_loop,)).start()
            self.loop = trans_loop
            SyncTransHandler.trans_loop = trans_loop
        else:
            self.loop = SyncTransHandler.trans_loop
        self.st_info = st_info
        # init bucket
        bucket = StrictRedis(host=st_info.redis_host, port=st_info.redis_port,
                             password=st_info.redis_password, db=st_info.redis_password, decode_responses=True)
        ok = bucket.ping()
        if not ok:
            raise Exception("redis 配置有误，无法连接到redis服务器...")
        self.bucket = bucket
        self.sess = None
        self.trans = None
        self.conn = None

    async def receive(self, client):
        """通过redis的订阅发布机制，在这里等待结果，并分发给不同方法处理
        """
        success = False
        while True:
            msg = client.get_message(ignore_subscribe_messages=True)
            if msg is None:
                await asyncio.sleep(0.005)
                continue
            data = json.loads(msg['data'])
            success = data['result']
            break
        client.close()  # 是否能真的断开连接，测试下 todo
        self.bucket.close()
        self.db_exc(success)

    def db_exc(self, success: bool):
        """执行,commit or rollback
        """
        if success:
            self.sess.commit()
            self.trans.commit()
        else:
            self.trans.rollback()
        self.sess.close()
        self.trans.close()
        self.conn.close()

    def notify_wait4result(self, sess, trans, conn):
        """当自己事务执行成功后 等待提交需要通知p-core
        到这里来说一定都是成功了的，等待事务提交或者 其他服务失败 - 回滚
        """
        self.sess = sess
        self.trans = trans
        self.conn = conn
        self.bucket.publish(self.st_info.sid, self.st_info.tid)
        # 保证先注册
        client = self.bucket.pubsub()
        client.subscribe(self.st_info.tid)  # 通知的是sid，订阅的是tid
        # 等待结果，只有在自己完事后才开始等待
        self.run_coro(self.receive(client))

    def run_coro(self, coro):
        if not iscoroutinefunction(coro):
            raise Exception("coro 不是一个协程方法。。。")
        asyncio.run_coroutine_threadsafe(coro, self.loop)
