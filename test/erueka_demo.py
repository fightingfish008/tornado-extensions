# coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web,tornado.gen
import py_eureka_client.eureka_client as eureka_client
from tornado.options import define, options
define("port", default=3333, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument('username', 'Hello')
        self.write(username + ', Administrator User1!')


if __name__ == "__main__":

    tornado.options.parse_command_line()
    #注册eureka服务
    eureka_server_list = "http://192.168.2.64:8761/eureka/"
    eureka_client.init_registry_client(eureka_server=eureka_server_list,
                            app_name="python-tornado-xyweb",
                            instance_port=3333)
    tornado.gen.sleep(2)
    app = tornado.web.Application(handlers=[(r"/info", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
