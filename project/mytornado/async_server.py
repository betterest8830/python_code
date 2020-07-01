# coding=utf8

import time
import datetime as dt

import tornado.gen
import tornado.httpserver
import tornado.ioloop
import tornado.web

# 同步方式
class SleepHandler2(tornado.web.RequestHandler):
    def get(self):
        time.sleep(3)
        # self.write('when i sleep')
        self.write(str(dt.datetime.now()))

# 异步方式
class SleepHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.sleep(3)
        self.write(str(dt.datetime.now()))


if __name__ == '__main__':
    app = tornado.web.Application(
        [
            (r'/sleep', SleepHandler),
        ],
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    print('server start')
    tornado.ioloop.IOLoop.instance().start()
