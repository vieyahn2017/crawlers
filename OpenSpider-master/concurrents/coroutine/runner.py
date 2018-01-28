__author__ = 'zhangxa'


'''
A runner is executor object which must implemeted run method.
'''
class Runner:
    def __init__(self,*args,**kwargs):
        self._args = args
        self.__kwargs = kwargs


    def run(self):
        raise NotImplementedError