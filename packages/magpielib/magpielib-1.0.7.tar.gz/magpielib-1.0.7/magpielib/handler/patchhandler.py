"""
    patch 的使用场景：1.不阻塞组流程，比如下订单的时候 异步更新用户订单数据情况，或者更新分销返利数据
                    2.耗时任务处理，比如文件组装
    另外，对于调用patch方来说，如果给pid说明调用方关注结果（比如websocket 需要等待patch耗时操作的结果）
    实现方会将自己的结果写到redis对应的pid字段中。当然整个交互是通过redis来实现的，不用http方式
总体约束：patch 中的task 方法是没有返回值的（方法本身返回成功失败）
        如果patch需要返回相关数据的话就将patch 方法写成rest 形式就好
"""
from magpielib.application import RESPONSE_OK
from magpielib.handler.handler_util import ReqUtil
from magpielib.handler.reqhandler import BaseReqHandler
from tornado.ioloop import IOLoop
from magpielib.util.log import get_logger
from magpielib.util.pcorewait import PatchWaitDealer, WaitPatchInfo
logger = get_logger("patch_handler")


class TaskHandler(BaseReqHandler):

    async def get(self):
        IOLoop.current().spawn_callback(
            self.patch_handler().dispatch, self.patch_handler,
            self.p, self.behavior, self.sync_trans, self.patch_wait, self.request.path, "Get")
        return self.j_response()

    async def post(self):
        IOLoop.current().spawn_callback(
            self.patch_handler().dispatch, self.patch_handler,
            self.p, self.behavior, self.sync_trans, self.patch_wait, self.request.path, "Post")
        return self.j_response()

    async def put(self):
        IOLoop.current().spawn_callback(
            self.patch_handler().dispatch, self.patch_handler,
            self.p, self.behavior, self.sync_trans, self.patch_wait, self.request.path, "Put")
        return self.j_response()

    async def delete(self):
        IOLoop.current().spawn_callback(
            self.patch_handler().dispatch, self.patch_handler,
            self.p, self.behavior, self.sync_trans, self.patch_wait, self.request.path, "Delete")
        return self.j_response()


class PatchHandler(ReqUtil):
    """task 通知调用方 调用成功或失败，如果调用方不关心结果的话，那么就发起报警
    整体交互都是和p-core 交互，调用方如果想得到结果也需要通过websocket访问p-core 等待结果
    """
    def __init__(self):
        super().__init__()
        self.p = None  # 参数
        self.behavior = None
        self.sync_trans = None  # 见BaseReqHandler 注释
        self.patch_wait = None  # # 见BaseReqHandler 注释
        self.patch_handler = None
        self.session = None
        self.j_response_data = {}
        self.uri = None
        self.method = None

    async def dispatch(self, patch_handler, p, b, st, pw, uri, method):
        self.patch_handler = patch_handler
        self.p = p
        self.behavior = b
        self.sync_trans = st
        self.patch_wait = pw
        self.uri = uri
        self.method = method
        # 判断是否要通知调用方结果
        if self.patch_wait:
            self.patch_wait_dealer = PatchWaitDealer.get_instance(WaitPatchInfo(self.patch_wait))
        msg = ""
        try:
            if method == "Get":
                await self.get()
            elif method == "Post":
                await self.post()
            elif method == "Put":
                await self.put()
            elif method == "Delete":
                await self.delete()
            else:
                raise Exception('never happen....')
        except Exception as e:
            msg = " patch 任务 异常**** %s" % str(e)
        if not msg and self.j_response_data is None:
            msg = "Patch方法实现错误-@请联系对应的服务编写人员->请按照j_response_data 形式给出正确结果"
        if not msg and self.j_response_data.get("data"):
            msg = "Patch方法实现错误-@请联系对应的服务编写人员->patch 只关注结果，不关注data ->%s" \
                  % self.j_response_data.get("data")
        if not msg and self.j_response_data.get("status") != RESPONSE_OK:
            msg = self.j_response_data.get("msg")
        if msg:
            logger.error("!!!!patch handler---error... %s", msg)
            if self.patch_wait_dealer:
                self.notify_to_caller(progress=1, msg=msg, success=False)
            return
        # 走到这里代表整体成功了，判断下最后有没有通知到
        if self.patch_wait_dealer and not self.patch_wait_dealer.done_notify_yet:
            self.notify_to_caller(progress=1, msg=self.j_response_data.get("msg"), success=False)
        logger.info("@@@ in patch done->:%s", self.j_response_data)

    def notify_to_caller(self, progress: float, msg="", success=False):
        """ 在同一个接口该方法可以多次被调用，以便传递progress（注意 progress >1 的时候就不通知调用方了；代表这个事件结束）
        当接收到 pcore 的patch_wait 时，业务处理过程中要通知调用方 可以通知过程的progress进度（最常见的是在调用完成通知 调用方结果）
        process: 0~1，!=1 这时候 可以传process msg 等信息；这个时候忽略success信息; == 1 代表结束

        **call_patch_wait4done 该方法和其对应，对于patch 和 rest 都有这个需求，故写 在 父类 ReqUtil 中实现了

        """
        self.patch_wait_dealer.notify(progress, msg, success)

    async def get(self, *args, **kwargs):
        """will impl by 业务层
        """
        raise Exception('to impl the do function')

    async def post(self, *args, **kwargs):
        """will impl by 业务层
        """
        raise Exception('to impl the do function')

    async def put(self, *args, **kwargs):
        """will impl by 业务层
        """
        raise Exception('to impl the do function')

    async def delete(self, *args, **kwargs):
        """will impl by 业务层
        """
        raise Exception('to impl the do function')

    def j_response(self, status=RESPONSE_OK, msg='', data=None, only4data=False, extra=None):
        from magpielib.util.helper import success_result, fail_result
        if status == RESPONSE_OK:
            json_response = success_result(data, self.uri, self.method, self.behavior)
        else:
            json_response = fail_result(status, msg, extra=extra)
        self.j_response_data = json_response
        if only4data:
            return json_response

    def write(self, chunk):
        """ 仿照 tornado RequestHandler 中方法
        兼容db中 deal_except handler.write(json.dumps(fail_error))
        """
        self.j_response_data = chunk
