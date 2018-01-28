__author__ = 'zhangxa'

from OpenSpider.configparser.xmlparser import XmlParser

'''
workflowconfig parse workflow config from file and sotre the result to a queue
'''
class WorkFlowConfig:
    def __init__(self,filename):
        self._file = filename
        self._workflowData = []

    def _loadWorkflowFile(self):
        self._
