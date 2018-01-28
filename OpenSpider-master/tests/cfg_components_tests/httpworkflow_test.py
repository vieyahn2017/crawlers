__author__ = 'zhangxa'

import os

import yaml

import unittest

class HttpWorkFlowComponentsTest(unittest.TestCase):
    def testRedisFactory(self):
        cfg = os.path.join('OpenSpider','cfg','httpworkflow','RedisRequestFactoryComponent.yaml')
        with open(cfg,'r') as fin:
            configs = yaml.load(fin)
        print(configs)

if __name__ == "__main__":
    unittest.main(warnings='ignore')