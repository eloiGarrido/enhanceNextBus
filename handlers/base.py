import tornado.ioloop
import tornado.web
import json
from tornado.concurrent import Future
from tornado import gen
import logging

# Initialize logger
logger = logging.getLogger('nextBus')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class MessageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('message')


def main():
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/api/message", MessageHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

