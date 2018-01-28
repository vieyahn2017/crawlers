__author__ = 'zhangxa'


'''
A concurrentManager should apply a class func who has a run method.
'''
class ConcurrentManger:
    def __init__(self,concurrents,runner,*args,**kwargs):
        self._concurrents = concurrents
        self._runner = runner
        self._args = args
        self._kwargs = kwargs

    def run(self):
        raise NotImplementedError
