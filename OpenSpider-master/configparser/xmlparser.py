__author__ = 'zhangxa'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from OpenSpider.configparser import ConfigParser

class XmlParser(ConfigParser):
    def parseConfig(self,filename):
        pass
