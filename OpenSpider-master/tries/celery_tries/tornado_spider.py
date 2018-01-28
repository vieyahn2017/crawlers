__author__ = 'zhangxa'

import tasks
from tornado import gen,web
from tornado.ioloop import IOLoop
import time
import tcelery

tcelery.setup_nonblocking_producer()
"""

@gen.coroutine
def hello_celery():
    a = yield gen.Task(sleep.apply_async,args=[2])
    print(a.get())

IOLoop.instance().run_sync(hello_celery)
"""
def hello():
    print("fuck")

@gen.coroutine
def test_async():
    yield gen.sleep(2)
    print("done")
    a = yield gen.Task(tasks.fetch_a_url.apply_async,args=["http://www.jd.com"])
    #a = yield gen.Task(tasks.sleep.apply_async,args=[3])
    print("done",a.result)
    yield gen.sleep(10)

IOLoop.instance().run_sync(test_async)