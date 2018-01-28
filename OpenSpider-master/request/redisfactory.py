__author__ = 'zhangxa'

from OpenSpider.request import RequestFactory
from OpenSpider.spiderQueue.driver import QueueDriverManage

class RedisRequestFactory(RequestFactory):
    def initialize(self,**settings):
        manger = QueueDriverManage(**settings)
        self.driver = manger.get_queue_driver()

    def makeRequest(self):
        return self.driver.get()


if __name__ == "__main__":
    settings = {"driver":"redis","driver_settings":{
        "host": "localhost",
            "port": 6379,
            "db": 1
    }}
    rf = RequestFactory(**settings)
