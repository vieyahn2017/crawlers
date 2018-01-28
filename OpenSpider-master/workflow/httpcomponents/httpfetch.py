__author__ = 'zhangxa'

from tornado import gen
from OpenSpider.workflow.compent import WorkFlowComponent

class HttpFetchComponent(WorkFlowComponent):
    @gen.coroutine
    def execute(self):
        print(self._input)