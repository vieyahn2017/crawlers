__author__ = 'zhangxa'

from tornado.gen import coroutine

from scrapy.utils.trackref import object_ref

class Request(object_ref):
    pass

'''
A requestFactory drive the program running by continuously fire requests.
A subclass should implement the makeRequest method and return a request object,the method should return a Future
if it may blocked.
'''
class RequestFactory:
    def __init__(self,**settings):
        self.settings = settings
        self.initialize(**settings)
        #self.start_flag = True

    #a hook function for subclass to initialize
    def initialize(self,**settings):
        pass

    def fireRequest(self):
        return self.makeRequest()
