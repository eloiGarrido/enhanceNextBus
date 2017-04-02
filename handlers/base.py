from tornado import gen
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httpclient
from tornado.concurrent import Future
import logging
import logging.config
import handlers.settings as settings
import json
import xmltodict
import datetime as dt
import time
# Initialize logger
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('nextBus')
# Init query count tracker
query_counter = {}
query_cache = {}
query_slow = {}


class MainHandler(tornado.web.RequestHandler):
    '''
    Fallback handler for / route
    '''
    def get(self):
        self.write("Welcome to nextBus Enhanced.\n" +
                   "<br>\nRequest information with the following query structure:\n<br>\n<br>"
                   "http://localhost:8888/publicJSONFeed?command=commandName&a=agencyTag&additionParams..")


class MessageHandler(tornado.web.RequestHandler):
    '''
    NextBus commands request handler
    '''
    @gen.coroutine
    def validate_command_and_increment(self, command):
        '''
        Validates query command and increases its use counter 
        :param command: Query command
        :return: None
        '''
        if command in settings.ACCEPTED_COMMANDS:
            if command in query_counter:
                query_counter[command] = query_counter[command] + 1
            else:
                query_counter[command] = 1

    @gen.coroutine
    def get(self):
        '''
        RESTful GET function. 
        :return: Displays NextBus query result in JSON format 
        '''
        # Validate and account for query calls
        yield self.validate_command_and_increment(self.get_argument('command', None))
        # Retrieve query arguments
        self.args = self.request.query
        # Prepare accepted nextBus url
        url = settings.WEB_ENDPOINT + str(self.args)

        if self.args in query_cache:
            logger.info('Accessing cached information')
            self.write(query_cache[self.args]['info'])
        else:
            yield self.nextBusClient(url)

    @gen.coroutine
    def profile_query(self, start, end):
        '''
        Store 5 slowest performed queries
        :param start: Start time of current query
        :param end: End time of current query
        :return: None
        '''
        query_duration = format(end-start)
        if len(query_slow) < 5:
            if self.args not in query_slow:
                query_slow[self.args] = query_duration
        else:
            if min(query_slow.values()) < query_duration:
                for key, val in query_slow.items():
                    if val == min(query_slow.values()):
                        del query_slow[key]
                        query_slow[self.args] = query_duration
                        break

    @gen.coroutine
    def nextBusClient(self, url):
        '''
        Asynchronous HTTP client and non-blocking query fetch
        :param url: Formatted URL
        :return: Result of URL fetch
        '''
        client = tornado.httpclient.AsyncHTTPClient()
        yield client.fetch(url, self.handle_request)

    @gen.coroutine
    def handle_request(self, response):
        '''
        Asynchronous request handler
        :param response: Response obtained from nextBus service call
        :return: Yields response from nextBus 
        '''
        if response.error:
            logger.error("Error:", response.error)
        else:
            start = time.time()
            data = xmltodict.parse(response.body.decode('utf-8'), xml_attribs=True)
            self.write(data)
            end = time.time()
            yield self.profile_query(start, end)
            query_cache[self.args] = {'info': json.dumps(data), 'time': dt.datetime.now()}
        self.finish()


class QueryCounterHanlder(tornado.web.RequestHandler):
    '''
    Request handler for the query counter endpoint
    '''
    @gen.coroutine
    def get(self):
        self.write(query_counter)


class SlowestQueriesHandler(tornado.web.RequestHandler):
    '''
    Request handler for the slowest queries endpoint
    '''
    @gen.coroutine
    def get(self):
        self.write(query_slow)


def make_app():
    '''
    Builds Tornado web server
    :return: tornado web app
    '''
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/publicJSONFeed", MessageHandler),
        (r"/queryCounter", QueryCounterHanlder),
        (r"/slowestQueries", SlowestQueriesHandler)
    ])


@gen.coroutine
def cleanCache():
    '''
    Clean expired cache entries
    :return: None
    '''
    now = dt.datetime.now()
    entries_to_delete = []
    for entry in query_cache:
        time_diff = now - query_cache[entry]['time']
        if time_diff.seconds >= 20:
            entries_to_delete.append(entry)
    for entry in entries_to_delete:
        del query_cache[entry]


@gen.coroutine
def cacheManager():
    '''
    Coroutine to periodically call cleanCache
    :return: 
    '''
    while True:
        nxt = gen.sleep(10)
        yield cleanCache()
        yield nxt


def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().spawn_callback(cacheManager)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
