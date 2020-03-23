#!/usr/bin/env python3

import os
import asyncio
import tornado
from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line, parse_config_file
import tornado.autoreload

import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from urls import handlers
from libs.utils import parse_config_file
from libs import redis
from libs import mongodb
from libs import mysql
import logging


class Application(web.Application):
    def __init__(self):
        # Prepare IOLoop class to run instances on asyncio
        tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOMainLoop')

        settings = dict(
            # debug=options.debug,
            # xsrf_cookies=options.xsrf_cookies,
            # cookie_secret=options.cookie_secret,
            # login_url=options.login_url,
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    define("env", default="")  # 配置文件
    parse_command_line()

    if options.env == "apple":
        logging.info("use apple conf")
        parse_config_file(os.path.join(os.path.dirname(__file__), "conf/apple_app.conf"))
    else:
        logging.info("error:  unknow conf")
        assert False

    my_app = Application()
    http_server = HTTPServer(
        my_app,
        idle_connection_timeout=options.idle_connection_timeout,
        xheaders=True
    )

    http_server.bind(int(options.port))
    http_server.start()
    loop = asyncio.get_event_loop()

    # my_app.settings['mongo'] = mongodb.connect()
    my_app.settings['redis'] = loop.run_until_complete(redis.connect(loop, 7))
    mysql_con_dict = dict()
    # mysql_con_dict["point_1"] = mysql.connect(options.mysql_doctor_db)

    # my_app.settings['mysql'] = mysql_con_dict

    loop.run_forever()


if __name__ == "__main__":
    main()
