import json
from tornado.httpclient import AsyncHTTPClient
from urllib import parse
from magpielib.application import RESPONSE_SERVICE_ERROR, RESPONSE_NO_METHOD_ERROR, \
    RESPONSE_OK, UNITTEST, SYNC_LOCAL_FUNC_ERROR
from magpielib.util.log import get_logger
from magpielib.util.pcorewait import PatchWaitDealer, WaitPatchInfo
from magpielib.application import INT_TRUE
from magpielib.service_map import ServiceConst
from asyncio import iscoroutine
from magpielib.util.pcoresync import SyncTransInfo, SyncTransDealer
logger = get_logger("reqUtil")

# http method
HTTP_POST = 'POST'
HTTP_GET = 'GET'
HTTP_PUT = 'PUT'
HTTP_DELETE = 'DELETE'


class ReqUtil(object):

    def __init__(self):
        self.request = None
        self.patch_wait_dealer = None

    def j_response(self, status=RESPONSE_OK, msg='', data=None, only4data=False, extra=None):
        """
        统一定义返回格式
        :param status: 返回错误码，统一定义const.py, beside auth
        :param msg: 异常信息，正常为空
        :param data:
        :param only4data:
        :param extra:
        :return:
        """
        raise Exception('must impl it ....')

    @staticmethod
    async def rest_fetch_util(host_uri, method, param=None, behavior='',
                              called_by='', usr_info=None, sync_trans=None, mock_data=None):
        """由于都是内网连接，这里不出有微服务调用其他微服务的三方调用场景
        :param host_uri:
        :param method:
        :param behavior:
        :param param: 参数 dict
        :param called_by: 一般是调用者的信息，比如uri
        :param usr_info: 用户信息
        :param sync_trans: 微事务同步
        :param behavior: 微事务同步
        :param mock_data: 单元测试，跳过微服务调用直接返回
        :return:
        """
        if UNITTEST and mock_data:  # 单元测试跳过微服务间的调用
            return RESPONSE_OK, mock_data
        http_client = AsyncHTTPClient()
        arguments = {}
        if method is None or host_uri is None or method == "" or host_uri == "":
            raise Exception("host_uri, method can not be empty!")
        if not param:
            param = {}
        arguments['p'] = json.dumps(param)
        if behavior:
            arguments['b'] = behavior
        if sync_trans:  # 微事务同步相关信息
            arguments['s'] = json.dumps(sync_trans)
        if usr_info:
            arguments['u'] = json.dumps(usr_info)
        logger.debug('in rest fetch->host_uri: %s, method: %s, arguments: %s', host_uri, method, arguments)
        error_msg = None
        response = None
        if method == HTTP_POST:
            arg_data = parse.urlencode(arguments)
            try:
                response = await http_client.fetch(host_uri, body=arg_data, method=method)
            except Exception as e:
                error_msg = RESPONSE_SERVICE_ERROR, str(e)
        elif method == HTTP_PUT:
            arguments['p'] = param
            arg_data = json.dumps(arguments)
            try:
                response = await http_client.fetch(host_uri, body=arg_data, method=method)
            except Exception as e:
                error_msg = RESPONSE_SERVICE_ERROR, str(e)
        elif method == HTTP_GET or method == HTTP_DELETE:
            flag = '&' if '?' in host_uri else '?'
            for key, value in arguments.items():
                if isinstance(value, str):
                    continue
                arguments[key] = json.dumps(value)
            uri_p = host_uri + '%s%s' % (flag, parse.urlencode(arguments))
            try:
                response = await http_client.fetch(uri_p, method=method)
            except Exception as e:
                error_msg = RESPONSE_NO_METHOD_ERROR, str(e)
        else:
            error_msg = RESPONSE_NO_METHOD_ERROR, 'method 不能为空！'
        if error_msg:
            return error_msg[0], '%s-%s:%s-%s' % (called_by, host_uri, method, error_msg[1])
        if response.code != 200:
            return RESPONSE_SERVICE_ERROR, response.error
        data = json.loads(str(response.body, encoding='utf-8'))
        if data.get('status') != RESPONSE_OK:
            logger.error("%s, %s", data.get('status'), 'in service:{}'.format(host_uri) + data.get('msg'))
            return data.get('status'), data.get('msg')
        return RESPONSE_OK, data.get('data')

    async def restful_fetch(self, host_uri, method, param=None, behavior='', usr_info=None, mock_data=None):
        """由于都是内网连接，这里不出有微服务调用其他微服务的三方调用场景
        :param host_uri:
        :param method:
        :param behavior:
        :param usr_info: 用户信息
        :param param: 参数 dict
        :param behavior: 微事务同步
        :param mock_data: 单元测试，跳过微服务调用直接返回
        :return:
        """
        return await ReqUtil.rest_fetch_util(
            host_uri, method, param, behavior, self.request.path, usr_info, None, mock_data)

    async def call_sync_trans(self, events, s_type="rest", local_sync_coro=None, mock_data=None):
        """ 调用微事务同步接口，参数如下(patch 和 rest 方法都会用到事务同步，故写到他们的父类中了）
        [
            ('order', "http://pod-order:3289/oiwie/jklsf", {
                "order_id": "332990032",
            }, Post, behavior),
            ('rebate', "http://pod-rebate:3282/dfe/esf", {
                'order_id': "332990032",
                'real_money': '${order.total_payment_price}',
                'order_time': '${order.create_time}'
            }, Put, behavior),
            ('', "http://pod-rebate:3282/dfe/234sx", {
                'xxx': "3333",
            }, Delete, behavior),
        ]
        local_sync_coro：和微事务同步执行本地方法，要失败都失败。和微事务一样，返回值会体现在label中
        """
        if len(events) == 0:
            raise Exception('事件不能为空，事件json格式参照注释')
        if len(events) == 1 and local_sync_coro is None:
            raise Exception('这里不需要异步任务调用同步，微事务同步，那么直接调用 rest_fetch方法即可')
        if s_type not in ('patch', 'rest'):
            raise Exception('微事务同步类型错误')
        if s_type != "rest" and local_sync_coro is not None:
            raise Exception('只有rest 方式才支持本地代码和微事务同步')
        if UNITTEST and mock_data:  # 兼容单元测试
            if local_sync_coro:
                label, coro = local_sync_coro
                result = await coro
                if label:
                    mock_data[label] = result
            return RESPONSE_OK, mock_data
        pes = []
        from magpielib.service_map import ServerName
        for event in events:
            label, host_url, params, method, behavior = event
            if method.upper() not in (HTTP_PUT, HTTP_POST, HTTP_DELETE):
                raise Exception('get 方法不涉及微事务同步。。。')
            pes.append({
                "Label": label, "HostUrl": host_url, "Method": method, "Params": params, "Behavior": behavior
            })
        p = {
            "Type": s_type, "Creator": ServerName, "Events": pes
        }
        label = None
        coro = None
        if local_sync_coro:
            label, coro = local_sync_coro
            if not iscoroutine(coro):
                raise Exception("sync_coro 必须是一个协程方法 的类方法")
            p["LocalSync"] = INT_TRUE
        status, data = await self.restful_fetch(
            ServiceConst.patchCore + "/patchCore/syncTransRegister", "POST", p)
        logger.info("***Sync Trans Sid ->%s", data.get("Sid"))
        if status != RESPONSE_OK:  # 失败了就不用处理 local_sync_coro 方法了
            return status, data
        if not local_sync_coro:
            if s_type != "rest":
                return status, data
            return status, data.get("LabelData")
        notify_data = data.get("YieldNotify")
        st = SyncTransInfo(notify_data)
        try:
            # pcore 中 根据local_sync_coro 放弃notify，在微服务中notify
            result = await coro  # 这里可能报异常，那就直接抛出来就好
        except Exception as e:
            # 代理pcore通知成功状态，失败了在上边直接发返回了
            SyncTransDealer.get_pcore_agent(st).proxy_notify_all(notify_data.get("tids"), str(e))
            return SYNC_LOCAL_FUNC_ERROR, "微事务同步本地方法同步失败->" + str(e)
        SyncTransDealer.get_pcore_agent(st).proxy_notify_all(notify_data.get("tids"))
        if label:
            data.get("LabelData")[label] = result
        return status, data.get("LabelData")

    async def call_patch_delay(self, event, delay):
        """ 不关注结果的异步调用  delay-延时x秒
        event 参照 call_patch_wait4done；当 delay =0 情况不存在，直接restful 调用就好了，不需要走pcore；
        """
        if delay < 3:
            raise Exception("delay 延时函数必须有值(3内延时没有实际意义）！否则请直接restful调用patch")
        host_url, params, method, behavior = event
        p_event = {
            "HostUrl": host_url, "Method": method, "Params": params, "Behavior": behavior
        }
        from magpielib.service_map import ServerName
        return await self.restful_fetch(ServiceConst.patchCore + "/patchCore/patchRegister", "POST", {
            "Event": p_event, "Creator": ServerName, "Delay": delay
        }, behavior="delay")

    async def call_patch_wait4done(self, event, callback_patch4done, callback_patch4progress=None):
        """调用方 调用patch 方法，并且等待结果(先调用pcore)
        ("http://pod-order:3289/oiwie/jklsf", {
                "order_id": "332990032",
            }, Post, behavior)
        """
        if not callback_patch4done:
            raise Exception('请提供回调成功函数...')
        host_url, params, method, behavior = event
        if method.upper() not in (HTTP_GET, HTTP_PUT, HTTP_POST, HTTP_DELETE):
            raise Exception('方法错误...')
        p_event = {
            "HostUrl": host_url, "Method": method, "Params": params, "Behavior": behavior
        }
        from magpielib.service_map import ServerName
        status, data = await self.restful_fetch(ServiceConst.patchCore + "/patchCore/patchRegister", "POST", {
            "Event": p_event, "Creator": ServerName
        }, behavior="wait")
        if status != RESPONSE_OK:
            return status, data
        #  接收pcore 返回值
        #       "Pid":      schedule.Pid,
        # 		"Host":     redis.Host,
        # 		"Port":     redis.Port,
        # 		"Password": redis.Password,
        # 		"Db":       redis.Db,
        self.patch_wait_dealer = PatchWaitDealer.get_instance(WaitPatchInfo(data))
        logger.info("@@@call_patch_and_wait call pcore success, and begin wait... pid=%s",
                    self.patch_wait_dealer.pid)
        await self.patch_wait_dealer. \
            wait4result(callback_patch4progress, callback_patch4done)
        return status, {}
