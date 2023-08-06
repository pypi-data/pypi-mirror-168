import asyncio
import json
from magpielib.util.log import get_logger
from magpielib.util.asynredis import AsyncRedisHandler
logger = get_logger("pcore-sync")


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
        self.redis_db = sync_trans.get('redis').get('db')


class SyncTransDealer(AsyncRedisHandler):

    def __init__(self, redis_host, redis_port, redis_password, redis_db):
        super().__init__(redis_host, redis_port, redis_password, redis_db)
        self.sess = None
        self.trans = None
        self.conn = None
        self.sid = None
        self.tid = None

    @staticmethod
    def get_instance(st_info: SyncTransInfo):
        if st_info is None or st_info.tid is None or st_info.sid is None \
                or st_info.redis_db is None or st_info.redis_host is None \
                or st_info.redis_password is None:
            raise Exception("st_info 不合法，没有经过前端框架层校验")
        dealer = SyncTransDealer(st_info.redis_host, st_info.redis_port, st_info.redis_password, st_info.redis_db)
        dealer.sid = st_info.sid
        dealer.tid = st_info.tid
        return dealer

    @staticmethod
    def get_pcore_agent(st_info: SyncTransInfo):
        if st_info.redis_db is None or st_info.redis_host is None \
                or st_info.redis_password is None:
            raise Exception("st_info 不合法，没有经过前端框架层校验")
        dealer = SyncTransDealer(st_info.redis_host, st_info.redis_port, st_info.redis_password, st_info.redis_db)
        dealer.sid = st_info.sid
        dealer.tid = st_info.tid
        return dealer

    async def receive(self, client):
        """通过redis的订阅发布机制，在这里等待结果，处理提交或者回滚
        """
        logger.info("@@@ start receive......")
        success = False
        while True:
            msg = client.get_message(ignore_subscribe_messages=True)
            if msg is None:
                await asyncio.sleep(0.005)
                continue
            logger.info("@@@ *****sync trans receive--->%s", msg)
            data = json.loads(msg['data'])
            success = True
            if data['result']:
                success = False
            break
        client.unsubscribe(self.tid)
        client.close()
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
        logger.info("@@@ * db_exc-该服务微事务结束 结果：%s", success)

    def notify_fail4patch(self, msg):
        """对于patch 方法 需要通知失败状态
        """
        logger.info("@@@notify_fail4patch... start publish.")
        self.bucket.publish(self.sid, json.dumps({
            "Sid": self.sid,
            "Tid": self.tid,
            "Ok": False,
            "Msg": msg,
        }))

    def notify_success4patch(self, sess, trans, conn):
        """对于patch 方法， 通知成功，发起订阅等待成功消息
        """
        logger.info("@@@notify_success4patch... start publish.")
        self.sess = sess
        self.trans = trans
        self.conn = conn
        self.bucket.publish(self.sid, json.dumps({
            "Sid": self.sid,
            "Tid": self.tid,
            "Ok": True,
            "Msg": "",
        }))
        # 保证先注册
        logger.info("@@@register redis subscribe client...")
        client = self.bucket.pubsub()
        client.subscribe(self.tid)  # 通知的是sid，订阅的是tid
        # 等待结果，只有在自己完事后才开始等待
        self.run_coro(self.receive(client))

    def proxy_notify_all(self, tids, result=""):
        """代理 patchCore 来做notify all，到这里一定是成功的，但是可能local方法是报错
        要不热就直接不执行local_sync_func方法了
        """
        for tid in tids:
            self.bucket.publish(tid, json.dumps({
                "result": result,  # 不传代表成功
            }))

    def wait_result4rest(self, sess, trans, conn):
        """对于rest 方法，不需要通知，直接等待结果就好
        """
        logger.info("@@@wait_result4rest... ->do not need publish<-.")
        self.sess = sess
        self.trans = trans
        self.conn = conn
        # 保证先注册
        client = self.bucket.pubsub()
        client.subscribe(self.tid)  # 通知的是sid，订阅的是tid
        # 等待结果，只有在自己完事后才开始等待
        self.run_coro(self.receive(client))
