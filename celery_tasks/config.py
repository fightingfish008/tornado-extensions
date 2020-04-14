from __future__ import absolute_import
import os
import sys
from tornado.options import options
from libs.utils import parse_config_file

args = sys.argv

mydict = {}
for i in range(1, len(args)):
    # All things after the last option are command line arguments
    arg = args[i].lstrip("-")
    name, equals, value = arg.partition("=")
    mydict[name] = value

if "env" in mydict.keys():
    if mydict["env"] == "product":
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/product_app.conf"))
    elif mydict["env"] == "dev":
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/dev_app.conf"))
    elif mydict["env"] == "test":
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/test_app.conf"))
    elif mydict["env"] == "apple":
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/apple_app.conf"))

    else:
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/dev_app.conf"))
elif "config" in mydict.keys():
    if mydict["config"] == "product_flag" or mydict["config"] == "product":
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/product_app.conf"))
    elif mydict["config"] == "dev_flag" or mydict["config"] == "dev":
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/dev_app.conf"))
    elif mydict["config"] == "test_flag" or mydict["config"] == "test":
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/test_app.conf"))
    elif mydict["config"] == "apple_flag " or mydict["config"] == "celery_tasks.apple_flag" :
        parse_config_file(os.path.join(os.path.dirname(__file__), "../conf/apple_app.conf"))
    else:
        print("无法匹配启动参数",mydict['config'])
# "schedule": crontab（）与crontab的语法基本一致
# "schedule": crontab(minute="*/10",  # 每十分钟执行
# "schedule": crontab(minute="*/1"),   # 每分钟执行
# "schedule": crontab(minute=0, hour="*/1"),    # 每小时执行

debug = True
cache_enabled = False

#redis
redis_host = options.redis_host
redis_port = options.redis_port
redis_password = options.redis_password
redis_db0 = options.redis_db0
redis_db1 = options.redis_db1
redis_db10 = options.redis_db10
redis_db11 = options.redis_db11
redis_db3 = options.redis_db3
redis_db4 = options.redis_db4
redis_db5 = options.redis_db5
redis_db6 = options.redis_db6
redis_db15 = options.redis_db15


#mysql


# 指定中间人broker地址
broker = 'redis://:' + redis_password + '@' + redis_host + ':' + str(redis_port) + '/' + str(redis_db5)
backend = 'redis://:' + redis_password + '@' + redis_host + ':' + str(redis_port) + '/' + str(redis_db4)
broker_url = 'redis://:' + redis_password + '@' + redis_host + ':' + str(redis_port) + '/' + str(redis_db3)
timezone = options.timezone
worker_hijack_root_logger = False  # celery默认开启自己的日志，可关闭自定义日志，不关闭自定义日志输出为空
result_expires = options.result_expires


# celery 日志配置
#celerylog = options.CELERYLOG
