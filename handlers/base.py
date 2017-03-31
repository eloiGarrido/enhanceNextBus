from tornado import gen
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httpclient
from tornado.concurrent import Future
import logging
import logging.config
import settings as settings
import json
import xmltodict

# Initialize logger
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('nextBus')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to nextBus Enhanced.\n" + "<br>\n")
        self.write('Request information with the following query structure:\n<br>\n<br>http://localhost:8888/'
                   'publicJSONFeed''?command=commandName&a=agencyTag&additionParams..')


class MessageHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):

        # Initialize Next Bus Handler object
        args = self.request.query
        url = settings.WEB_ENDPOINT + str(args)
        client = tornado.httpclient.AsyncHTTPClient()
        yield client.fetch(url, self.handle_request)

    def handle_request(self, response):
        if response.error:
            print("Error:", response.error)
        else:
            data = xmltodict.parse(response.body.decode('utf-8'), xml_attribs=True)
            self.write(data)
        self.finish()


def main():
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/publicJSONFeed", MessageHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
