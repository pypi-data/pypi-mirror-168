import logging
import logging.config
log_base_name = None

#  log 相关配置如下：
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p'
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },

        # "file": {
        #     "class": "logging.handlers.RotatingFileHandler",
        #     "level": "INFO",  #
        #     "formatter": "simple",
        #     "filename": None,
        #     'mode': 'w+',
        #     "maxBytes": 1024*1024*5,  # 5 MB
        #     "backupCount": 20,
        #     "encoding": "utf8"
        # }
    },
    "loggers": {
        "console": {
            "level": "DEBUG",  # 这个地方不控制，交给具体的handler控制级别
            "handlers": ["console"],
            "propagate": "no"
        }
    }
}


def __set_log_name(log_name):
    """在配置中加入log_name实例文件，并修改文件结构
    :param log_name:
    :return:
    """
    a_log = {
        "level": "DEBUG",
        # "handlers": ["console", "file"],
        "handlers": ["console"],
        "propagate": "no"
    }
    LOGGING.get('loggers')[log_name] = a_log  # 设置log实例配置
    # LOGGING.get('handlers').get('file')['filename'] = \
    #     os.path.join(log_path, 'logs/{}.log'.format(log_name))  # 设置log存储位置


def init_logger(log_name, is_debug=False):
    """ 获取logger
    :param log_name: 根据不同的service 获取不同的logger，在启动的时候初始化
    :param is_debug: 这个控制文件中是否记录debug，控制台始终会有debuglog
    :return:
    """
    # from coms import ENV, ENV_PROD, ENV_LOCAL
    # if ENV != ENV_LOCAL:
    # is_debug = True  # only in un-product env  show debug logs...
    global log_base_name
    if log_base_name is not None:
        return
    __set_log_name(log_name)
    if is_debug:
        LOGGING.get('handlers').get('console')['level'] = 'DEBUG'
    # log_file = os.path.dirname(LOGGING.get('handlers').get('file').get('filename'))
    # if not os.path.exists(log_file):
    #     os.makedirs(log_file)
    logging.config.dictConfig(LOGGING)
    log_base_name = log_name


def get_logger(name):
    """
    获取对应log名字
    :param name:
    :return:
    """
    log = logging.getLogger("{}.{}".format(log_base_name, name))
    return log
