import logging
from libs.handler import EntityHandler
from libs.const import MsgCode
import json
from tornado.options import options

logger = logging.getLogger('myapp')


def cache(func):
    def inner(self, *args, **kwargs):
        # ret = yield self.redis.get('index')
        # if ret:
        #     self.write(ret)
        #     return
        func(self, *args, **kwargs)
        # r.set('index', self._data_html[0], ex=10)  # 设置过期时间为10秒
    return inner


# GET /extension/check
class ExtensionCheck(EntityHandler):

    async def solution(self, lis):
        argumentDict = dict()
        for argument in lis.keys():
            argumentDict[argument] = self.get_argument(argument, None)

        res = "AnonyMousUse:"+self.request.path
        res += json.dumps(argumentDict)

        # 检查是否有缓存
        resRedis = await self.redis.get(res)
        logger.info("asafdafdafd")

        if resRedis is None:
            logger.info("insert redis")

            retData1 = dic = {"fun": "hello tornado extension"}
            await  self.redis.setex(res, seconds=options.expires_time, value=json.dumps(dic))
            return retData1
        else:
            retData1 = json.loads(resRedis)
            return retData1

    # @cache
    async def get(self):

        arguments = self.request.arguments
        retData= await self.solution(arguments)
        return self.v2_write_json(code=MsgCode.SUCCESS, msg="success", data=retData)

handlers = [
    (r"^/extension/check", ExtensionCheck, dict(collection='test_scripts')),
]
