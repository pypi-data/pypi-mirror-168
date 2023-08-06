from magpielib.util.log import get_logger
from redis import StrictRedis
logger = get_logger("bucket")


class Reds(object):
    bucket = None

    def __init__(self):
        if self.bucket is None:
            raise Exception('bucket can not be None!')

    def clear4debug(self):
        # 单元测试专用！
        self.bucket.flushdb()

    @classmethod
    def ge_db(cls, db):
        if cls.bucket:
            return cls.bucket
        from magpielib.application import config
        redis = config.Redis
        bucket = StrictRedis(host=redis.Host, port=redis.Port, password=redis.Password, db=db, decode_responses=True)
        cls.bucket = bucket
        logger.info('>>>>>>>bucket REDIS_HOST is:%s', bucket)
        return cls.bucket
