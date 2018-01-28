__author__ = 'zhangxa'

import tcelery
from tornado.ioloop import IOLoop
from tornado import gen,queues

import time
import configparser

from OpenSpider.SpiderCelery.celery import app
from OpenSpider.SpiderCelery import tasks
from OpenSpider.spiderQueue.driver import QueueDriverManage


tcelery.setup_nonblocking_producer()

base_url = 'http://www.lagou.com'
concurrency = 10

@gen.coroutine
def main():
    yield gen.sleep(3)
    '''
    settings = {"driver":"redis","driver_settings":{
            "host": "localhost",
                "port": 6379,
                "db": 1
        }}
    '''
    settings = {}
    config = configparser.ConfigParser()
    config.read('settings.cfg')
    settings['driver'] = config['QUEUE_DRIVER']['driver']

    driver_settings = {}
    driver_settings['host'] = config['DRIVER_SETTINGS']['host']
    driver_settings['port'] = config['DRIVER_SETTINGS']['port']
    driver_settings['db'] = int(config['DRIVER_SETTINGS']['db'])
    settings['driver_settings'] = driver_settings

    manger = QueueDriverManage(**settings)
    q = manger.get_queue_driver()

    @gen.coroutine
    def fetch_url():
        cur_url = yield q.get()
        try:
            print("fetching url:%s" % cur_url)
            urls = yield gen.Task(tasks.fetch_a_url.apply_async,args=[cur_url])
            url_lists = urls.result
            print("cur_url urls:",cur_url,url_lists)
            if not url_lists:
                return
            for url in url_lists:
                yield q.put(url)
        except Exception as e:
            print("a exception:",e)

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put(base_url)

    for _ in range(concurrency):
        worker()

    yield q.join(None)

if __name__ == "__main__":
    IOLoop.current().run_sync(main)