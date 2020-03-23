# -*- coding:utf-8 -*-

import json
import logging

from tornado.web import RequestHandler, HTTPError
from tornado.options import options
from libs.const import MsgCode, PageCode
# from common import LogConfig
import time

logger = logging.getLogger('myapp')


class BaseHandler(RequestHandler):
    def initialize(self):
        pass
        self.redis = self.settings['redis']
        # self.mongo = self.settings['mongo']
        # self.mysql = self.settings['mysql']

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def write_json(self, msg, code):
        if MsgCode.SUCCESS == code:
            _msg = {'code': code, 'msg': "", 'data': msg}

        else:
            _msg = {'code': code, 'msg': msg, 'data': {}}
        if options.debug:
            logger.info(_msg)
        self.finish(_msg)

    def v2_write_json(self, msg, code, data=None):
        _msg = {'code': code, 'msg': msg, 'data': data}
        if options.debug:
            logger.info(_msg)
        self.finish(_msg)


class NEWBaseHandler(BaseHandler):
    def initialize(self):
        super(NEWBaseHandler, self).initialize()
        # self.mysqldoctor = self.settings['mysql']['doctor']
        # self.myredis = self.settings['redis']

    async def prepare(self):
        # get_current_user cannot be a coroutine, so set
        # self.current_user in prepare instead.
        content_type = self.request.headers.get("Content-Type")
        if content_type and content_type.startswith("application/json"):
            # self.json_dict = json.loads(self.request.body.decode('utf-8'))
            pass
        else:
            self.json_dict = None

        if self.request.method not in ("HEAD", "GET"):
            pass


class EntityHandler(NEWBaseHandler):

    def initialize(self, collection):
        self.collection = collection

        super(EntityHandler, self).initialize()


    async def create(self, document):
        return await self.mongo.insert_one(self.collection, document)

    async def _delete(self, filter):
        return await self.mongo.delete(self.collection, filter)

    async def update_one(self, filter, kwargs):
        return await self.mongo.modify(self.collection, filter, kwargs)

    async def update(self, filter, kwargs):

        return await self.mongo.update(self.collection, filter, kwargs)

    async def retrieve(self, filter):
        return await self.mongo.find_one(self.collection, filter)


class ErrorHandler(RequestHandler):
    """Default 404: Not Found handler."""
    def prepare(self):
        super(ErrorHandler, self).prepare()
        raise HTTPError(404)


class NotFondHandler(BaseHandler):
    def get(self):
        self.write("This page ``{}``is not Found".format(self.request.path))