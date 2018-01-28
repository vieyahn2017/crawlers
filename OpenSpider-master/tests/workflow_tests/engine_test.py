__author__ = 'zhangxa'

import unittest

from tornado.ioloop import IOLoop

from OpenSpider.concurrents.coroutine.conruntinemanager import CoruntineManager
from OpenSpider.workflow.engine import WorkflowEngine

class WorkflowEngine_test(unittest.TestCase):
    def test_workflow_run(self):
        engine = WorkflowEngine(['OpenSpider.workflow.compent.WorkFlowComponent',
                                 'OpenSpider.workflow.compent.WorkFlowComponent1'])
        cm = CoruntineManager(10,engine,1)
        cm.run()

        IOLoop.instance().start()

if __name__ == "__main__":
    unittest.main(warnings='ignore')
