import os
import yaml
from yaml import SafeLoader

# 服务地址发现，每个服务都需要维护，从本地环境变量中获取
ServiceConst = None
ServerName = ""


def parse_server_addr(path=None):
    """
    解析全局的环境变量；兼容单元测试
    """
    global ServiceConst
    if ServiceConst:
        return
    from magpielib.application import UNITTEST
    if UNITTEST:
        with open(path, encoding='utf-8') as f:
            data = yaml.load(f, Loader=SafeLoader)
    else:
        data = os.environ
    _ServiceConst = type('__SERVICES__', (object,), dict())()
    for k, v in data.items():
        _ServiceConst.__setattr__(k, v)
    ServiceConst = _ServiceConst

