import logging
from libs.handler import EntityHandler
from libs.const import MsgCode

logger = logging.getLogger('myapp')


# GET /info
class SystemInfo(EntityHandler):

    async def get(self):
        username = self.get_argument('username', 'Hello')
        return self.v2_write_json(code=MsgCode.SUCCESS, msg="success", data=username+", Administrator User!")

handlers = [
    (r"^/info", SystemInfo, dict(collection='test_scripts')),
]