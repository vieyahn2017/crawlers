__author__ = 'zhangxa'

import os

import tcelery
from tornado.ioloop import IOLoop
from tornado import gen
import yaml

from OpenSpider.workflow.engine import WorkflowEngine
from OpenSpider.resource.manager import ResourceManager
from OpenSpider.concurrents.coroutine.runner import Runner

tcelery.setup_nonblocking_producer()

base_url = 'http://www.lagou.com'
concurrency = 10

@gen.coroutine
def main():
    #yield gen.sleep(3)
    class CoruntineRunner(Runner):
        @gen.coroutine
        def run(self):
            print('run begin')
            yield gen.sleep(1)
            print('run end!')

    with open('./OpenSpider/main.yaml','r') as fin:
        configs = yaml.load(fin)

    globals = configs['global']
    concurrency = int(globals['concurrency'])
    concurrent_manager = ResourceManager.getResource(globals['concurrent_manager'])

    engine_settings = configs['engine']
    engine_cls = ResourceManager.getResource(engine_settings['name'])

    workflow_cfg_path = os.path.join('OpenSpider','cfg',engine_settings['workflow'])
    with open(workflow_cfg_path,'r') as fin:
        workflow_cfg = yaml.load(fin)

    engine = engine_cls(workflow_cfg)
    cm = concurrent_manager(concurrency,engine)
    cm.run()

    yield gen.sleep(10)

if __name__ == "__main__":
    IOLoop.current().run_sync(main)