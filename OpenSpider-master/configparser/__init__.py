__author__ = 'zhangxa'


class ConfigParser:
    def __init__(self,filename):
        self._file = filename
        self._configs = {}

    """
    a ConfigParser should implemented this method to parse configs from a file and return a map
    """
    def parseConfig(self,filename):
        raise NotImplementedError

    def getConfig(self,key):
        if not self._configs:
            self._configs = self.parseConfig(self._file)
        return self._configs.get(key)