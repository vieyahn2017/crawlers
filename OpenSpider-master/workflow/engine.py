__author__ = 'zhangxa'
import os

from tornado import gen
import yaml

from OpenSpider.concurrents.coroutine.runner import Runner
from OpenSpider.resource.manager import ResourceManager

class WorkflowEngine(Runner):
    def __init__(self,workflows,**settings):
        self._workflows = workflows
        self._settings = settings

    '''
    We must define coroutine here,because every component in workflow should execute one by one.
    So the component class also should implement its execute method in a coroutine
    '''
    @gen.coroutine
    def run(self):
        input = None
        for component in self._workflows:
            lst = component.split('.')
            settings = {}
            cfg_file = os.path.join(lst[0],'cfg','httpworkflow',lst[-1]+'.yaml')
            if os.path.exists(cfg_file):
                with open(cfg_file,'r') as fin:
                    settings = yaml.load(fin)
            cls_comp = ResourceManager.getResource(component)
            obj_comp = cls_comp(input,**settings)
            input = yield obj_comp.execute()

    def executeElements(self,workflow):
        for comp in workflow:
            comp.execute()