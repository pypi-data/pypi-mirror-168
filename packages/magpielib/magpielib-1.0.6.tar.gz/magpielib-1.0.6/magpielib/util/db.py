# 目前框架，只支持 tornado 和 task 两种形式
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as Session_  # 为了去警告！
from functools import wraps
from magpielib.util.log import get_logger
from magpielib.application import RESPONSE_SERVICE_ERROR, RESPONSE_OK, SESS_DEBUG
import json
from magpielib.util.pcoresync import SyncTransDealer, SyncTransInfo

Session = Session_  # class 对象
trans_loop = None
logger = get_logger('db_conf')
engine: any
engine = None


class _Session(Session_):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_only = False
        self.is_has_commit = False

    def commit(self):
        if self.read_only:
            raise Exception('-read_only can not commit...')
        self.is_has_commit = True
        super().commit()


def db_config(mysql):
    global engine, Session
    if engine is not None:  # 说明已经被初始化过来
        logger.debug('___this db has been initialized!')
        return engine

    dbconf = {'pool_timeout': mysql.PoolTimeout, 'echo': False, 'pool_size': mysql.PoolSize}
    engine = create_engine(mysql.Uri, **dbconf)
    engine.connect()
    logger.info('db_config- the uri is:%s, pool_size->%s', mysql.Uri, mysql.PoolSize)
    Session = sessionmaker(engine, class_=_Session)
    return engine


def load_dbsession(*, read_only=True, ignore_result=True):
    """类的获取session 通常服务于tornado，兼容协程
    --important协程只支持class 形式！
    ignore_trans 普通调用 做微事务，要不还要返回dict
    """
    def wraps_(func):
        if read_only:
            @wraps(func)
            async def _wraps(handler, *args, **kwargs):
                return await obtain_sess(func, handler, *args, **kwargs)
        else:
            @wraps(func)
            async def _wraps(handler, *args, **kwargs):
                return await obtain_sess_trans(func, handler, ignore_result, *args, **kwargs)
        return _wraps
    return wraps_


async def obtain_sess_trans(f, handler, ignore_result=True, *args, **kwargs):
    """只针对协程，相关业务需要在 base或task中实现
    """
    result = None
    sync_trans_info = None
    while True:
        conn = engine.connect()
        sess = Session(bind=conn, autoflush=False)
        trans = conn.begin()
        try:
            handler.session = sess
            if handler.sync_trans:
                sync_trans_info = SyncTransInfo(handler.sync_trans)
            _result = await f(handler, *args, **kwargs)
            result = handler.j_response_data
            # 统一数据提交
            if sync_trans_info is None:
                deal_commit(handler, sess, trans, conn)
                break
            if ignore_result:  # 兼容migrate
                if not isinstance(result, dict):
                    raise Exception('请实现BaseReqHandler 或 SyncReqHandler 类方法')
                if result.get('status') == RESPONSE_OK:
                    deal_commit(handler, sess, trans, conn, sync_trans_info)
                else:
                    sync_trans_info = None  # 业务失败，走finally 断开此次提交
                result = None
            else:  # ignore_result false 代表关注返回值，这时候就忽略事务同步了
                deal_commit(handler, sess, trans, conn, sync_trans_info)
                result = _result
            break
        except Exception as e:  # 连接失败重新获取连接！
            if 'OperationalError' in str(type(e)) and 'MySQL server' in str(e):
                continue
            else:
                trans.rollback()  # 回滚后 再 close 释放资源
                sess.close()
                trans.close()
                conn.close()
                result = e
                break
        finally:
            if not sync_trans_info:  # 不为空的时候 异步 等待微事务同步
                sess.close()
                trans.close()
                conn.close()

    if isinstance(result, Exception):
        if SESS_DEBUG:
            raise result
        return deal_except(f, result, handler, sync_trans_info)
    return result


async def obtain_sess(f, handler, *args, **kwargs):
    """只针对协程，相关业务需要在 base或task中实现
    """
    while True:
        async def doit():
            sess = None
            try:
                sess = Session()
                sess.read_only = True
                handler.session = sess
                return await f(handler, *args, **kwargs)
            finally:
                sess.close()
        if SESS_DEBUG:
            return await doit()
        try:
            return await doit()
        except Exception as e:  # 连接失败重新获取连接！
            if 'OperationalError' in str(type(e)) and 'MySQL server' in str(e):
                continue
            else:
                return deal_except(f, e, handler)


def deal_except(f, e, handler, sync_trans_info=None):
    from magpielib.util.helper import fail_result
    logger.error('db->deal_except f:%s, e:%s, self:%s', f, e, handler)
    fail_error = fail_result(RESPONSE_SERVICE_ERROR, 'func is:%s, error is:%s' % (f, str(e)))
    if 'pymysql.err.DataError' in str(e):
        fail_error = fail_result(RESPONSE_SERVICE_ERROR, '数据异常')
    handler.write(json.dumps(fail_error))  # 兼容 reqHandler 和 syncHandler
    if sync_trans_info and handler.patch_handler is not None:
        # 需要微事务同步，并且 是 patch 方法，我们才需要通知 pcore 失败状态；
        # rest 方式直接通过返回结果就可以知道该事件结果了
        SyncTransDealer.get_instance(sync_trans_info).notify_fail4patch(fail_error)


def deal_commit(handler, sess, trans, conn, sync_trans_info=None):
    """异步提交commit事务
    """
    if not sync_trans_info:
        sess.commit()
        trans.commit()
        return
    if sync_trans_info:
        if handler.patch_handler is not None:
            # 上面的 close 会在finally 中 完成，下边的是非阻塞的微事务同步
            SyncTransDealer.get_instance(sync_trans_info).notify_success4patch(sess, trans, conn)
            return
        SyncTransDealer.get_instance(sync_trans_info).wait_result4rest(sess, trans, conn)
