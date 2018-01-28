__author__ = 'zhangxa'

from tornado import gen
from ..request import Request

class Component:
    def __init__(self,input,**kwargs):
        self._input = input
        self._kwargs = kwargs
        self.initialize(**kwargs)

    def initialize(self,**kwargs):
        pass

    @gen.coroutine
    def execute(self):
        pass

class WorkFlowComponent(Component):
    @gen.coroutine
    def execute(self):
        print('WorkFlowComponent run')
        yield gen.sleep(1)
        print('WorkFlowComponent run end')

class WorkFlowComponent1(Component):
    @gen.coroutine
    def execute(self):
        print('WorkFlowComponent1 run')
        yield gen.sleep(1)
        print('WorkFlowComponent1 run end')