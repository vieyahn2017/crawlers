
from tornado import gen
from OpenSpider.workflow.compent import WorkFlowComponent
from OpenSpider.request.redisfactory import RedisRequestFactory

class RedisRequestFactoryComponent(WorkFlowComponent):
    def initialize(self,**kwargs):
        self._factory = RedisRequestFactory(**kwargs)

    @gen.coroutine
    def execute(self):
        request = yield self._factory.makeRequest()
        return request


