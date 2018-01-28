__author__ = 'zhangxa'

from importlib import import_module
'''
This class is mainly used for instantiate a class dynamically
'''
class ResourceManager:
    @staticmethod
    def getResource(path):
        try:
            dot = path.rindex('.')
        except ValueError:
            raise ValueError("Error loading object '%s': not a full path" % path)

        module,name = path[:dot],path[dot+1:]
        mod = import_module(module)

        try:
            obj = getattr(mod,name)
        except AttributeError:
            raise NameError("Module %s doesn't define any object named :%s" % (module,name))

        return obj

