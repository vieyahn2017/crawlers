__author__ = 'zhangxa'

from tornado.locks import Event
import collections

"""
QueueDriverManage根据配置的driver来动态地产生对应的queue_driver
"""
class QueueDriverManage:
    def __init__(self,**settings):
        self.settings = settings

    def get_queue_driver(self):
        driver = self.settings.get("driver")
        driver_settings = self.settings.get("driver_settings")
        queue_driver = QueueDriverFactory.create_queue(driver,**driver_settings)
        return queue_driver(**driver_settings)

class QueueEmpty(Exception):
    pass

"""
QueueDriver用于实现队列接口，主要提供get,put,save接口。
"""
class QueueDriver:
    def __init__(self,**settings):
        self.settings = settings
        self._finished = Event()
        self._getters = collections.deque([])  # Futures.
        self._putters = collections.deque([])
        self.initialize(**settings)

    def initialize(self,**settings):
        pass

    def over(self):
        self._finished.set()

    def save(self):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()

    def put(self):
        raise NotImplementedError()

    def join(self,timeout=None):
        return self._finished.wait(timeout)

"""
QueueDriver工厂，根据driver名称，返回对应的类.
driver所在的模块名应该为以下形式：
OpenSpider.spiderQueue.%squeue%driver.lower()

"""
class QueueDriverFactory(object):
    @staticmethod
    def create_queue(driver,**settings):
        module_name = 'OpenSpider.spiderQueue.%squeue'%driver.lower()
        module = __import__(module_name,globals(),locals(),['object'],0)
        cls = getattr(module,'%sQueue'%driver.capitalize())
        if not 'QueueDriver' in [ base.__name__ for base in cls.__bases__ ]:
            raise InvalidQueueDriverException('%s not found in current spiderQueue driver implements '% driver)
        return cls

class InvalidQueueDriverException(Exception):
    pass


