import configparser

IMPORT_BASE = """
# target_metadata = None
import sys
from os.path import abspath, dirname
path = {src_path}
sys.path.append(path)
{import_base}
target_metadata = Base.metadata
"""


def alter(file, old_str, new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def init_alembic(file_db, cwd_path, tool_path, src_path, logger):
    """判断时候有alembic，没有则重新创建，重点将 uir改成当前的uir
    """
    import os
    # alembic_command = '/opt/venv/bin/alembic' if not debug else 'alembic'
    alembic_command = 'alembic'
    os.chdir(cwd_path)  # 将目录切换到当前！
    db_tag, uri, import_base = file_db
    if not os.path.exists(tool_path):
        os.makedirs(tool_path)
        os.chdir(tool_path)
        do_shell('%s init alembic' % alembic_command, logger)  # 刚刚创建的时候alembic 初始化
        # 修改env文件！
        env_path = tool_path + 'alembic/env.py'
        alter(env_path, 'target_metadata = None',
              IMPORT_BASE.format(import_base=import_base, src_path=src_path))
    conf = configparser.ConfigParser()
    conf.read(tool_path + 'alembic.ini')
    conf.set('alembic', 'sqlalchemy.url', uri)
    with open(tool_path + 'alembic.ini', 'w') as fw:
        conf.write(fw)
    # 执行对应的 数据库更新操作！
    os.chdir(tool_path)
    do_shell('%s revision --autogenerate -m "update_db%s"' % (alembic_command, db_tag), logger)
    do_shell('%s upgrade head' % alembic_command, logger)


def do_shell(cmd, logger):
    """log 可实时输出
    """
    logger.info('cmd: %s', cmd)
    import subprocess

    def run_process(exe):
        p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            # returns None while subprocess is running
            retcode = p.poll()
            line = p.stdout.readline()
            try:
                yield str(line, encoding='utf-8')
            except UnicodeDecodeError:
                yield str(line, encoding='gbk')  # 兼容windows
            if retcode is not None:
                break

    for _line in run_process(cmd.split()):
        if _line:
            logger.info(_line[:-1])
