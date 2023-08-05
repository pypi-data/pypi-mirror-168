import json
from tornado.web import RequestHandler
from urllib import parse
from magpielib.application import RESPONSE_OK, RESPONSE_VALIDATE_ERROR, PARSE_ERROR_REQ_P
from magpielib.handler.handler_util import ReqUtil
from magpielib.util.helper import validate_jschema_fields
from magpielib.util.log import get_logger
from magpielib.util.api_models import ShRouter
from magpielib.util.table_query import TableSearchSchema, TableLimitSchema, TableSortSchema
logger = get_logger('BaseReqHandler')


class _ValidateHandler:
    """
    校验p_schema 和 admin_auth
    """
    SyncTransSchema = {
        "desc": "sync_trans 参数格式校验",
        "type": "object",
        "properties": {
            "sid": {"type": "string"},
            "tid": {"type": "string"},
            "redis": {
                "type": "object",
                "properties": {
                    "host": {"type": "string"},
                    "port": {"type": "string"},
                    "password": {"type": "string"},
                    "db": {"type": "integer"},
                },
                "required": ["host", "port", "password", "db"]
            }

        },
        "required": ["sid", "tid", "redis"]
    }

    @staticmethod
    def v_p_schema(req_handler, p_schema):
        """整体校验apps的参数 涉及到 sync_trans data校验
        """
        # tableschema 的标签替换
        _ValidateHandler.inject_table(p_schema)
        err = validate_jschema_fields(req_handler.p, p_schema)
        if err:
            return 'p参数错误-%s-%s-->%s' % (req_handler.__class__, req_handler.request.method, err)
        if not req_handler.sync_trans:
            return None
        # 校验 sync_trans 事务同步传参正确性
        err = validate_jschema_fields(req_handler.sync_trans, _ValidateHandler.SyncTransSchema)
        if err:
            return 's参数错误-:%s-%s-->%s' % (req_handler.__class__, req_handler.request.method, err)
        return None

    @staticmethod
    def inject_table(p_schema):
        """表单标准格式参数注入
        """
        if not p_schema:
            return
        if p_schema.get("properties").get("$tableSearch"):
            p_schema.get("properties")["$tableSearch"] = json.loads(TableSearchSchema)
        if p_schema.get("properties").get("$tableSort"):
            p_schema.get("properties")["$tableSort"] = json.loads(TableSortSchema)
        if p_schema.get("properties").get("$tableLimit"):
            p_schema.get("properties")["$tableLimit"] = json.loads(TableLimitSchema)


class BaseReqHandler(RequestHandler, ReqUtil):
    """very important notice:
    综述：为了实现RESTful api, 该类实现了对
        application
        auth统一用户认证，
        和数据库的基本配置，
        消息队列，及微服务数据库同步配置
    对于每个service应该copy一份该类，来实现除用户授权以外的相关配置
    1. (a).在子类中实现的get/post/etc... 在使用@auth_verify 装饰器后，
        新加其他装饰器，装饰器必须用@functools.wraps(func)保留原函数信息
       (b).一旦使用了@auth_verify方法后，该方法为登陆后使用方法，并且对应相关权限。
       ps.auth_group中为或的关系
    2. 对于登陆后信息，usr_info再之后的接口中可以正常使用！
    3. RESTful api 对于每个service应该copy一份该类，来实现对数据库的配置
    """

    def data_received(self, chunk):
        # 去除警告，无实际意义
        pass

    def __init__(self, application, request, **kwargs):
        super(BaseReqHandler, self).__init__(application, request, **kwargs)
        self.p = None  # 参数
        self.behavior = None
        self.sync_trans = None  # 微事务同步传递参数，包括 sid, tid; redis info两类信息
        self.patch_wait = None  # 异步调用结果等待，包括 pid, redis info两类信息
        self.is_third_party = False
        self.patch_handler = None  # 异步调用handler，在patch_handler中使用(用此来判断是否是patch handler）
        # 数据库session
        self.session = None
        self.handlerClass = None
        self.j_response_data = {}

    def prepare(self):
        """参数解析，合法性校验（包括三方系统调用穿透），很简单只有两步
        0. 为pcore 预调用获取接口类型
        1. p、b参数解析（判断是否是third_party情况，只这一种）
        2. 获取ShRouter 并进行schema 校验
        """
        if self.request.method == 'OPTIONS':
            self.finish()
            return
        req_uri = self.request.path
        req_method = self.request.method
        logger.debug('req_uri = %s, method = %s', req_uri, req_method)
        # 1
        ok, is_third_party, router_type, user_info = self.parse_param()
        if router_type:
            self.set_status(200, "预调用handler 类型成功")
            self.finish(self.j_response(data={"type": router_type}, only4data=True))
            return
        self.is_third_party = is_third_party
        if not ok:
            self.set_status(201, "p 参数不合法")
            self.finish(self.j_response(PARSE_ERROR_REQ_P, "p 参数不合法", only4data=True))
            return
        if is_third_party:
            return
        ok, data = self.find_uri_conf(req_uri, req_method, self.behavior, user_info)
        if not ok:
            self.set_status(202, data)
            self.finish(self.j_response(
                PARSE_ERROR_REQ_P, "interface error! -%s, %s, %s, %s"
                                   % (req_uri, req_method, self.behavior, data), only4data=True))
            return
        # 2
        error = _ValidateHandler.v_p_schema(self, data)
        if error is not None:
            self.set_status(203, "p schema校验失败")
            self.finish(self.j_response(
                RESPONSE_VALIDATE_ERROR, msg="p schema校验失败 %s" % str(error),
                only4data=True, data={'error_detail': error}))
            logger.warning("%s, %s, %s->p schema校验失败 %s" % (
                self.request.path, self.request.method, self.behavior, str(error)))
            return

    def find_uri_conf(self, req_uri, req_method, behavior, user_info):
        """通过 uri method， behavior 来定位一个 detail(对应的配置）
           解析svcs_info
           该方法会在taskHandler 中重写，因为对应的配置变了
        """
        from magpielib.util.api_models import ShRouter
        sh_router = ShRouter.get_sh_router(req_uri)  # 走到这里一定是注册成功了，不用判空
        rd = sh_router.get_detail(req_method, behavior)
        if rd is None:
            return False, 'router detail not found!'
        if sh_router.type.upper() == "PATCH":
            self.patch_handler = sh_router.patch_handler
        elif sh_router.type.upper() == "GATE":
            if rd.auth[0].upper() not in ("OFFER", "PUBLIC"):
                if not user_info:
                    return False, '@@@*please login first!!!'
                # 将u参数拼接到p参数中, 前提是GATE类型接口，只有GATE类型才涉及到鉴权-进而才有u
                if isinstance(user_info, dict):
                    self.p["__user_info__"] = user_info
                else:
                    self.p["__user_info__"] = json.loads(parse.unquote(user_info))
        return True, rd.p_schema

    def parse_param(self):
        """ 将参数解析出来，并且判断参数是否合规
        """
        # 判断是否是系统外部调用
        is_third_party = self.get_argument('__isThirdParty__', None)
        if is_third_party:
            logger.info("@@@__isThirdParty__... %s", self.request.path)
            return True, True, None, None  # 三方系统调用
        # 请求参数校验
        try:
            user_info = None
            if self.request.method == 'PUT':
                if self.request.files:
                    self.p = {}
                else:
                    arguments = json.loads(str(self.request.body, encoding='utf-8'))
                    self.p = arguments.get('p')
                    user_info = arguments.get('u')
                    self.behavior = arguments.get('b')
                    self.sync_trans = arguments.get('__st__')
                    self.patch_wait = arguments.get('__pw__')
            else:
                # import base64
                p = self.get_argument('p', None)
                if p:
                    p = json.loads(parse.unquote(p))  # 获取系统指定格式参数
                else:
                    p = {}
                self.p = p  # 赋值p参数  important
                user_info = self.get_argument('u', None)
                self.behavior = self.get_argument('b', None)
                sync_trans = self.get_argument('__st__', None)
                if sync_trans:
                    sync_trans = json.loads(parse.unquote(sync_trans))
                    self.sync_trans = sync_trans
                patch_wait = self.get_argument('__pw__', None)
                if patch_wait:
                    patch_wait = json.loads(parse.unquote(patch_wait))
                    self.patch_wait = patch_wait
        except Exception as e:
            logger.warning('in _is_argument_qualified:%s, type:%s' % (e, type(e)))
            return False, False, None, None
        # 是否是 预调用获取接口类型
        sh_router = ShRouter.get_sh_router(self.request.path)  # 走到这里一定是注册成功了，不用判空
        if self.p.get("__p-handler-type__"):
            logger.info("@@@__p-handler-type__... %s", self.request.path)
            return True, False, sh_router.type, None
        return True, False, None, user_info

    def on_finish(self):
        pass

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
        from magpielib.util.helper import success_result, fail_result
        if self.is_third_party:  # 兼容三方系统调用
            self.write(json.dumps(data))
            return
        if status == RESPONSE_OK:
            json_response = success_result(data, self.request.path, self.request.method, self.behavior)
        else:
            json_response = fail_result(status, msg, extra=extra)
        self.j_response_data = json_response
        if only4data:
            return json_response
        self.write(json.dumps(json_response))
