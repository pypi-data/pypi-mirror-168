import os
from magpielib.util.api_models import ShRouter
import yaml
from yaml.loader import SafeLoader
from magpielib.util.log import get_logger
logger = get_logger("parse")


def parse_config(path, key_instances: dict):
    """解析配置文件
    """
    with open(path, encoding='utf-8') as f:
        data = yaml.load(f, Loader=SafeLoader)
    # server = Server()
    # server.generate(data.get("Server"))
    for key, instance in key_instances.items():
        instance.generate(data.get(key))


# 解析inner 接口yaml文件
def parse_apis(path, server_name):
    """解析apis
    """
    if not path:
        return []
    file_list = []
    get_yaml_files(path, file_list)
    sh_routers = []
    for file in file_list:
        with open(file, encoding='utf-8') as f:
            data = yaml.load(f, Loader=SafeLoader)
            sh_router = ShRouter()
            sh_router.generate(data, server_name)
            sh_routers.append(sh_router)
    return sh_routers


# 获取folder下所有的yaml文件
def get_yaml_files(folder, file_list: list):
    file = os.listdir(folder)
    for f in file:
        real_url = os.path.join(folder, f)
        if os.path.isfile(real_url):
            if real_url.endswith(".yaml"):
                file_list.append(real_url)
        elif os.path.isdir(real_url):
            get_yaml_files(real_url, file_list)


class BaseConfig(object):
    def generate(self, info: dict):
        for k, v in info.items():
            self.__setattr__(k, v)

    def __str__(self):
        return self.__dict__.__str__()


def parse_obj_config(path, config, *subconfig):
    """解析config to obj
    """
    conf = {}
    for item in subconfig:
        conf[item.__class__.__name__] = item
    parse_config(path, conf)
    config.generate(conf)
    return config

