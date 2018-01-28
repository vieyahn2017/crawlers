__author__ = 'zhangxa'

import unittest

from tornado import ioloop,gen

from OpenSpider.request import RequestFactory
from OpenSpider.spiderQueue.driver import QueueDriverFactory,QueueDriverManage
from OpenSpider.spiderQueue.redisqueue import RedisQueue
from OpenSpider.request.redisfactory import RedisRequestFactory

'''
class RedisRequestFactory(RequestFactory):
    settings = {"driver":"redis","driver_settings":{
        "host": "localhost",
            "port": 6379,
            "db": 1
    }}
    manger = QueueDriverManage(**settings)
    driver = manger.get_queue_driver()

    @classmethod
    def makeRequest(cls):
        return cls.driver.get()
'''

class RedisReuqest_test(unittest.TestCase):
    def test_redisRequest(self):
        settings = {"driver":"redis","driver_settings":{
        "host": "localhost",
            "port": 6379,
            "db": 1
    }}

        @gen.coroutine
        def test_async():
            rf = RedisRequestFactory(**settings)
            while True:
                request = yield rf.fireRequest()
                print('a request:%s'%request)

        ioloop.IOLoop.instance().run_sync(test_async)

if __name__ == "__main__":
    unittest.main(warnings='ignore')