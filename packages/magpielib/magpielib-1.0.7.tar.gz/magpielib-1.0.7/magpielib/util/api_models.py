from magpielib.util.helper import parse_instance_from_str


class RouterDetail(object):

    def __init__(self, ):
        self.method = None
        self.auth = []
        self.link_auth = []
        self.behavior = None
        self.p_schema = None
        self.r_schema = None

    def generate(self, info: dict):
        """将配置文件转化成 RouterDetail
        """
        self.method = info.get('Method')
        self.auth = info.get('Auth')
        self.link_auth = info.get('LinkAuth')
        self.behavior = info.get('Behavior')
        self.p_schema = info.get('PSchema')
        self.r_schema = info.get('RSchema')
        if not self.method:
            raise Exception("method 不能为空！_>info:%s" % info)
        if not self.p_schema:
            self.p_schema = {}

    def __str__(self):
        return f"     RouterDetail.method:{self.method} \n " \
               f"    RouterDetail.auth:{self.auth} \n " \
               f"    RouterDetail.link_auth:{self.link_auth} \n " \
               f"    RouterDetail.behavior:{self.behavior} \n " \
               f"    RouterDetail.p_schema:{self.p_schema} \n " \
               f"    RouterDetail.r_schema:{self.r_schema} \n " \
               f"    _______________________________@"


# service handler router
class ShRouter(object):
    _handler_map = {}

    def __init__(self):
        self.uri = ""
        self.handler = None
        self.patch_handler = None
        self.type = None
        self.router_details = []

    def generate(self, info: dict, server_name: str):
        """将配置文件转回成ShRouter
        """
        self.uri = info.get('Uri')
        self.type = info.get('Type').upper()
        if not self.type:
            raise Exception("handler-> type 不能为空 (REST, PATCH, GATE):%s" % info)
        if not self.uri:
            raise Exception("uri 不能为空！_>info:%s" % info)
        if not self.uri.startswith("/" + server_name + "/"):
            raise Exception("uri 必须以config.yaml文件中server.name 开头！uri is:%s" % self.uri)
        if self.type == "PATCH":
            from magpielib.handler.patchhandler import TaskHandler
            self.handler = TaskHandler
            # 专门针对patch
            _handlerClass = parse_instance_from_str(info.get('Handler'))
            if _handlerClass is None:
                raise Exception("未找到patch-> %s 对应的Handler->%s，请检查配置文件..." % (self.uri, info.get('Handler')))
            self.patch_handler = _handlerClass
        else:
            self.handler = parse_instance_from_str(info.get('Handler'))
        if self.handler is None:
            raise Exception("未找到rest-> %s 对应的Handler->%s，请检查配置文件..." % (self.uri, info.get('Handler')))
        for detail in info.get('Details'):
            router_detail = RouterDetail()
            router_detail.generate(detail)
            self.router_details.append(router_detail)
        if not self.router_details:
            raise Exception("detail不能为空！Uri-> %s" % self.uri)
        # 便于应用层通过uri 得到对应的所有信息
        ShRouter._handler_map[self.uri] = self
        # 校验
        self.validate()

    def validate(self):
        if self.type != "GATE":
            for detail in self.router_details:
                if detail.auth:
                    raise Exception("对于非网关方法来说，不需要指定auth！")
            return None
        for detail in self.router_details:
            if not detail.auth:
                raise Exception("对于gate方法来说，必须有指定auth！")

    def get_detail(self, method: str, behavior):
        """对应一个uri，通过method 和 behavior 就可以定位到一个detail
        进而得到对应的p_schema 或一些其他信息，比如 svcs_info 和
        """
        if not behavior:
            behavior = None
        for detail in self.router_details:
            if detail.method.upper() == method and detail.behavior == behavior:
                return detail
        return None

    @staticmethod
    def get_sh_router(uri):
        """通过 uri 获取ShRouter
        """
        return ShRouter._handler_map.get(uri)

    def __str__(self):
        router_detail_str = ""
        for router_detail in self.router_details:
            router_detail_str += str(router_detail) + '\n'
        return f"\n" \
               f"@****ShRouter.Uri:{self.uri} \n " \
               f"****ShRouter.Handler:{self.handler} \n " \
               f"****ShRouter.Details:\n{router_detail_str}" \
               f"**********************************@"


def log_routers(sh_routers: [], logger):
    for sh_router in sh_routers:
        logger.info("***---is: %s", sh_router)
