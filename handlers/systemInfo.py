import logging

from py_eureka_client import eureka_client

from libs.handler import EntityHandler
from libs.const import MsgCode

logger = logging.getLogger('myapp')


# GET /info
class SystemInfo(EntityHandler):

    async def get(self):
        username = self.get_argument('username', 'Hello')
        eureka_server_list = "http://192.168.2.64:8761/eureka/"
        eureka_client.init_discovery_client(eureka_server_list)
        res = eureka_client.do_service("python-tornado-xyweb",service="/info", return_type="string")
        print("result of other service" + res)
        return self.v2_write_json(code=MsgCode.SUCCESS, msg="success", data=username+", Administrator User!")

handlers = [
    (r"^/info", SystemInfo, dict(collection='test_scripts')),
]