import logging
import random

from py_eureka_client import eureka_client

from libs.handler import EntityHandler
from libs.const import MsgCode
from celery_tasks.sms.tasks import send_sms_code
logger = logging.getLogger('myapp')
import tcelery

tcelery.setup_nonblocking_producer()


# GET /smscode
class SystemInfo(EntityHandler):

    async def get(self):
        mobile = self.get_argument('mobile', '15014210589')
        sms_code = '%06d' % (random.randint(0, 999999))
        send_sms_code.delay(mobile, sms_code)
        return self.v2_write_json(code=MsgCode.SUCCESS, msg="success", data="短信发送中！！！")

handlers = [
    (r"^/smscode", SystemInfo, dict(collection='test_scripts')),
]