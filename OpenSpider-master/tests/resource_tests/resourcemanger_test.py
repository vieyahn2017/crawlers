__author__ = 'zhangxa'

import unittest

from OpenSpider.resource.manager import ResourceManager
from OpenSpider.workflow.compent import Component

class ResourceMangerTest(unittest.TestCase):
    def test_import(self):
        compent_cls = ResourceManager.getResource('OpenSpider.workflow.compent.Component')
        self.assertIs(compent_cls,Component)

if __name__ == "__main__":
    unittest.main(warnings='ignore')
