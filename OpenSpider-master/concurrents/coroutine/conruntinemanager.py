__author__ = 'zhangxa'

from tornado import gen

from OpenSpider.concurrents.manager import ConcurrentManger
from OpenSpider.concurrents.coroutine.runner import Runner

class CoruntineManager(ConcurrentManger):
    def run(self):
        for i in range(self._concurrents):
            self.coroutine()

    @gen.coroutine
    def coroutine(self):
        self._runner.run()


if __name__ == "__main__":
    from tornado.ioloop import IOLoop
    class CoruntineRunner(Runner):
        @gen.coroutine
        def run(self):
            print('run begin')
            yield gen.sleep(1)
            print('run end!')


    cm = CoruntineManager(10,CoruntineRunner(),1)
    cm.run()

    IOLoop.instance().start()