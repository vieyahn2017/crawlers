__author__ = 'zhangxa'

from OpenSpider.SpiderCelery.celery import app
from OpenSpider.SpiderCelery.tasks import fetch_a_url

import tcelery

from tornado import gen
from tornado.ioloop import IOLoop

import unittest

class Celery_worker_test(unittest.TestCase):
    def setUp(self):
        tcelery.setup_nonblocking_producer()

    def test_celery_tornado(self):
        @gen.coroutine
        def test_async():
            yield gen.sleep(2)
            a = yield gen.Task(fetch_a_url.apply_async,args=["http://www.jd.com"])
            #a = yield gen.Task(tasks.sleep.apply_async,args=[3])
            self.assertIsNotNone(a.result)
        print("run")
        IOLoop.instance().run_sync(test_async)

if __name__ == "__main__":
    unittest.main(warnings='ignore')