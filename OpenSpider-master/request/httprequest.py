__author__ = 'zhangxa'

from ..request import Request

'''
HttpRequest should have a dispatcher called HttpRequestDispatcher
'''
class HttpRequest(Request):
    def __init__(self,url):
        self._url = url
