"""
tornado 单元测试，基于原生的unittest，针对同步方法unittest的所有特性都可用
针对异步方法，tornado.test 给出两个方案：
1.AsyncTestCase 测试异步方法
2.AsyncHTTPTestCase 测试异步的请求
"""
from tornado import testing
import json
from urllib import parse
from magpielib.application import RESPONSE_OK
from magpielib import application
from magpielib.util.log import get_logger

application.UNITTEST = True  # 标识单元测试
application.SESS_DEBUG = True
logger = get_logger('AsyncHTTPTestCase')


class UnTestBaseHandler(testing.AsyncHTTPTestCase):
    """
    AsyncHTTPTestCase基础类，在这个类中封装了
    1.数据库，reds，初始化，清除etc...
    """
    # 全局变量，一个进程内会将startup和测试框架相关联
    init_application = None
    init_param = []

    def get_app(self):
        """这里完成uri的注册，否则测试类不知道哪些接口可以直接调用
        """
        if UnTestBaseHandler.init_application is None:
            logger.info('impl in subclass...')
            raise NotImplementedError
        return UnTestBaseHandler.init_application(*UnTestBaseHandler.init_param)

    def deal_fetch(self, uri, arguments: dict, method, ignore_assert=False):
        """ 单元测试获取数据 工具方法
        """
        response = None
        if method == 'POST':
            for key, value in arguments.items():
                if isinstance(value, str):
                    continue
                arguments[key] = json.dumps(value)
            arg_data = parse.urlencode(arguments)
            logger.info('uri === >>>>>%s ', uri)
            response = self.fetch(uri, method=method, body=arg_data)
        elif method == 'PUT':
            response = self.fetch(uri, method=method, body=json.dumps(arguments))
        elif method == 'GET' or method == 'DELETE':
            flag = '&' if '?' in uri else '?'
            for key, value in arguments.items():
                if isinstance(value, str):
                    continue
                arguments[key] = json.dumps(value)
            uri_p = uri + '%s%s' % (flag, parse.urlencode(arguments))
            response = self.fetch(uri_p, method=method)
            logger.info('@@@ request === >>>>> >>>>>>> = %s -  %s - %s', uri_p, method, arguments)
        # 解析response
        if response is None:
            raise Exception('miss http method: %s' % method)
        logger.info("@@@ response === >>>>> >>>>>>> = %s", str(response.body, 'utf-8'))
        if response.code != 200:
            self.assertEqual(response.code, 200, msg=response.error)
        # 如果有异常直接抛出来
        raw_data = json.loads(str(response.body, encoding='utf-8'))
        logger.info('@@@@@%s-%s raw_data is: %s', uri, method, raw_data)
        if ignore_assert:  # 交给前端校验！
            if raw_data.get('status') == RESPONSE_OK:
                return raw_data.get('status'), raw_data.get('data')
            else:
                return raw_data.get('status'), raw_data.get('msg')
        self.assertEqual(raw_data.get('status'), RESPONSE_OK, msg='%s, %s, %s' % (uri, method, raw_data.get('msg')))
        return raw_data.get('data')  # 数据都封装在data中...
