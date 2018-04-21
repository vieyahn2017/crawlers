#!/usr/bin/python
#coding=utf-8

# Version 1 by Dongwm 2013/01/10
# 脚本作用：gevent

import gevent.monkey
gevent.monkey.patch_all()
from gevent.queue import Empty, Queue
import gevent
from common import Crawler

class GeventLine(object):

    def __init__(self, workQueue, timeout=1, **kwargs):
        self.timeout = timeout #线程在结束前等待任务队列多长时间
        self.workQueue = workQueue

    def run(self):
        '''重载run方法'''
        while True:
            try:
                callable, args = self.workQueue.get(timeout=self.timeout) #从工作队列中获取一个任务
                res = callable(*args)  #执行的任务
                print res
            except Empty:
                break
            except Exception, e:
            	print e
                return -1

class GeventPool(object):

	def __init__(self, num_of_threads):
	         self.workQueue = Queue()
	         self.threads = []
	         self.__createThreadPool(num_of_threads)
	 
	def __createThreadPool(self, num_of_threads):
	    for i in range(num_of_threads):
	         thread = GeventLine(self.workQueue)
	         self.threads.append(gevent.spawn(thread.run))


	def wait_for_complete(self):
	    '''等待所有线程完成'''

	    while len(self.threads):
	        thread = self.threads.pop()
	        thread.join()
	    gevent.shutdown()
	 
	def add_job( self, callable, *args):
	    '''增加任务,放到队列里面'''
	    self.workQueue.put((callable, args))

def main():
	tp = GeventPool(10) 
	crawler = Crawler(tp)
	crawler.work()

if __name__ == '__main__':

    import timeit
    t = timeit.Timer("main()") 
    t.repeat(3, 10)
