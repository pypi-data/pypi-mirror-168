# 应用于各个app之间的工具类
import uuid
from math import radians, cos, sin, asin, sqrt
from magpielib.util.log import get_logger
import importlib
from jsonschema import validate

logger = get_logger('helper')
_req_loop = None


def gen_uuid():
    """
    生成数据库的uuid
    :return:
    """
    return uuid.uuid1().hex


def success_result(data, uri, method, behavior):
    """ 接口统一返回 成功数据的格式
    """
    data = {} if data is None else data
    if not isinstance(data, dict):
        raise Exception('j_response data must be dict!  %s' % data)
    from magpielib.application import RESPONSE_OK
    json_response = {
        'status': RESPONSE_OK,
        'msg': '',
        'data': data
    }
    logger.debug('---%s, %s, %s--success_result:%s', uri, method, behavior)
    return json_response


def fail_result(e, ed, extra=None):
    """接口统一返回 失败数据的格式
    """
    if extra:
        ed = '%s %s' % (ed, extra)
    json_response = {
        'status': e,
        'msg': ed,
        'data': {}
    }
    logger.debug('-******-*******--fail_result:%s, %s', e, ed)
    return json_response


def parse_instance_from_str(package_path):
    """
    通过配置文件的包名，解析对应的module class
    """
    if not package_path:
        return None
    module_name = ".".join(package_path.split(".")[0:-1])
    instance_name = package_path.split(".")[-1]
    module = importlib.import_module(module_name)
    try:
        instance = getattr(module, instance_name)
    except AttributeError:
        return None
    return instance


def validate_jschema_fields(data, schema):
    """
    校验后端请求接收的 json
    :param data:
    :param schema:
    :return:
    """
    if schema is None:
        return None
    try:
        validate(data, schema)
    except Exception as e:
        return str(e)


def get_show_time(total_seconds, hs='时', ms='分', ss='秒'):
    """根据固定秒数，返回对应的 时分秒
    """
    total_seconds = int(total_seconds)
    hour = total_seconds // 3600
    mini = (total_seconds % 3600) // 60
    second = (total_seconds % 60)
    return "{hour}{hs}{mini}{ms}{second}{ss}".\
        format(hour=hour, mini=mini, second=second, hs=hs, ms=ms, ss=ss)


class Error(object):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return str(self.info)


def deal_dict_datetime(data, tag_key='is_date_time',
                       tag_value='value', is_validate=True):
    """把对应tag的值timestamp 的value 改成datetime 类型
    """
    def _deal_datetime(_data):
        from datetime import datetime
        if not isinstance(_data, dict):
            return
        for key, value in _data.items():
            if isinstance(value, dict):
                _deal_datetime(value)
            elif isinstance(value, list):
                for av in value:
                    _deal_datetime(av)
            else:
                if key == tag_key and value:
                    if isinstance(_data.get(tag_value), float) or isinstance(_data.get(tag_value), int):
                        _data[tag_value] = datetime.fromtimestamp(_data.get(tag_value))
                    elif is_validate:
                        raise Exception('date time format wrong!')
                pass
    _deal_datetime(data)


def get_curr_month_str():
    """
    返回当前时间的月份值比如 201803，用于数据库统计，目前财务单，和预充值中使用
    :return:
    """
    from datetime import datetime
    now = datetime.now()
    group_time = now.strftime('%Y-%m')
    return group_time


def gen_numstr(len_):
    """
    生成len_位的纯数字字符串
    :param len_:
    :return:
    """
    import random
    return str(random.randint(0, pow(10, len_) - 1)).zfill(len_)


def gen_str(len_):
    """
    生成对应位数的随机字符串
    :param len_:
    :return:
    """
    import random
    import string
    return ''.join(random.sample(string.ascii_letters + string.digits, len_))


def gen_uppercase_str(len_):
    """
    生成对应位数的随机数字大写字母组合字符串
    :param len_:
    :return:
    """
    import random
    import string
    return ''.join(random.sample(string.ascii_uppercase + string.digits, len_))


def gen_str_num4more(num=1, lenth=8):
    """生成多个指定长度的字母数字组合字符串"""
    items = set()
    while True:
        items.add(gen_uppercase_str(lenth))
        if len(items) >= num:
            break
    return list(items)


def generate_salt_key():
    """
    生成user表中的 salt_key 用于密码加密和token生成
    added by conghl
    :return:
    """
    return gen_str(6)


def get_iso_8601(expire):
    """文件上传的时候使用
    """
    from datetime import datetime
    gmt = datetime.fromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt


def get_password_encode(password):
    import hashlib
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


def gen_str_all_asc(len_):
    """生成对应位数的随机字符串
    :param len_:
    """
    import random
    import string
    return ''.join(random.sample(string.ascii_letters + string.digits, len_))


def get_host_ip():
    """获取本机IP
    """
    import socket
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        if s:
            s.close()
    return ip


def get_last_month(time_month):
    """
    获取上个月时间
    :param time_month:
    :return:
    """
    from datetime import datetime
    date_month = datetime.strptime(time_month, "%Y-%m")
    if date_month.month-1 < 1:
        time_month = date_month.replace(month=12, year=date_month.year-1).strftime("%Y-%m")
    else:
        time_month = date_month.replace(month=date_month.month - 1).strftime("%Y-%m")
    return time_month


def get_last_day(time_day):
    """
    获取前一天
    :param time_day:
    :return:
    """
    from datetime import datetime, timedelta
    date_day = datetime.strptime(time_day, "%Y-%m-%d") + timedelta(days=-1)
    result = date_day.strftime('%Y-%m-%d')
    return result


def remove_exponent(num):
    return num.to_integral() if num == num.to_integral() else num.normalize()


def get_transfer_str4xml(ori_str):
    if ori_str is None:
        return ''
    ori_str = ori_str.replace('&', '&amp;')
    ori_str = ori_str.replace('>', '&gt;')
    ori_str = ori_str.replace('<', '&lt;')
    ori_str = ori_str.replace("'", '&apos;')
    ori_str = ori_str.replace('"', '&quot;')
    return ori_str


def get_func_packg(func):
    """获取方法的包名称
    """
    return '%s.%s' % (func.__module__, func.__name__)


def get_client_ip(req, default_ip):
    """获取客户端IP
    """
    val = req.headers.get('X-Forwarded-For')
    if not val:
        return default_ip
    val = val.replace(' ', '')
    return val.split(',')[0]


def geodistance(lng1, lat1, lng2, lat2):
    """根据经纬度计算两点间距离 单位是米"""
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000
    return dis


async def download_file(url, path=None, raw=False, retry=3):
    """文件下载到指定路径, 是否直接返回，默认重试三次
    """
    from tornado.httpclient import AsyncHTTPClient
    http_client = AsyncHTTPClient()
    try:
        response = await http_client.fetch(url)
    except Exception as e:
        if retry == 0:
            raise Exception('download file failed! e:%s', e)
        logger.error("download_file Error: %s" % e)
        await download_file(url, path, raw, retry-1)
    else:
        if raw:
            return response.body
        with open(path, "wb") as code:
            code.write(response.body)

