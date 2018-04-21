#!/usr/bin/python
#coding=utf-8

# Version 1 by Dongwm 2013/01/10
# 脚本作用：多线程



import time
import threading
import Queue
from common import Crawler

#lock = threading.Lock()   #设置线程锁


class MyThread(threading.Thread):

    def __init__(self, workQueue, timeout=1, **kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        self.timeout = timeout #线程在结束前等待任务队列多长时间
        self.setDaemon(True)  #设置deamon,表示主线程死掉,子线程不跟随死掉
        self.workQueue = workQueue
        self.start() #初始化直接启动线程

    def run(self):
        '''重载run方法'''
        while True:
            try:
                #lock.acquire() #线程安全上锁 PS:queue 实现就是线程安全的，没有必要上锁 ,否者可以put/get_nowait
                callable, args = self.workQueue.get(timeout=self.timeout) #从工作队列中获取一个任务
                res = callable(*args)  #执行的任务
                #lock.release()  #执行完,释放锁 
            except Queue.Empty: #任务队列空的时候结束此线程
                break
            except Exception, e:
                return -1


class ThreadPool(object):

    def __init__(self, num_of_threads):
         self.workQueue = Queue.Queue()
         self.threads = []
         self.__createThreadPool(num_of_threads)
 
    def __createThreadPool(self, num_of_threads):
        for i in range(num_of_threads):
             thread = MyThread(self.workQueue)
             self.threads.append(thread)

    def wait_for_complete(self):
        '''等待所有线程完成'''
        while len(self.threads):
            thread = self.threads.pop()
            if thread.isAlive():  #判断线程是否还存活来决定是否调用join
                thread.join()
     
    def add_job( self, callable, *args):
        '''增加任务,放到队列里面'''
        self.workQueue.put((callable, args))
def main():

    tp = ThreadPool(10) 
    crawler = Crawler(tp)
    crawler.work()

if __name__ == '__main__':

    import timeit
    t = timeit.Timer("main()") 
    t.repeat(3, 10)

    
    

