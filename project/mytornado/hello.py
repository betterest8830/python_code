# coding=utf8

import tornado.ioloop
import tornado.web
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, tornado")
        # self.write("<h1>Hello, tornado</h1>")
        self.render('base.html')


class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('500.html', msg="后台有错")


def make_app():
    return tornado.web.Application(
        [
            (r'/', MainHandler),
            (r'/500', ErrorHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        debug=True,
    )


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
