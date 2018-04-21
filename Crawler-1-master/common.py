#!/usr/bin/python
#coding=utf-8

# Version 1 by Dongwm 2013/01/10
# 脚本作用：多线程抓取
# 方式： lxml + xpath + requests

import requests
from  cStringIO import StringIO
from lxml import etree

class Crawler(object):

    def __init__(self, app):
        self.deep = 2  #指定网页的抓取深度        
        self.url = '' #指定网站地址
        self.key = 'by' #搜索这个词
        self.tp = app #连接池回调实例
        self.visitedUrl = [] #抓取的网页放入列表,防止重复抓取

    def _hasCrawler(self, url): 
        '''判断是否已经抓取过这个页面'''
        return (True if url in self.visitedUrl else False)
     
    def getPageSource(self, url, key, deep): 
        ''' 抓取页面,分析,入库.
        '''
        if self._hasCrawler(url): #发现重复直接return
            return 
        else:
            self.visitedUrl.append(url) #发现新地址假如到这个列
        r = requests.get('http://localhost/%s' % url)
        encoding = r.encoding #判断页面的编码
        result = r.text.encode('utf-8').decode(encoding)
	    #f = StringIO(r.text.encode('utf-8'))
        try:
            self._xpath(url, result, ['a'], unicode(key, 'utf8'), deep) #分析页面中的连接地址,以及它的内容
            self._xpath(url, result, ['title', 'p', 'li', 'div'], unicode(key, "utf8"), deep) #分析这几个标签的内容
        except TypeError: #对编码类型异常处理,有些深度页面和主页的编码不同
            self._xpath(url, result, ['a'], key, deep)
            self._xpath(url, result, ['title', 'p', 'li', 'div'], key, deep)
        return True

    def _xpath(self, weburl, data, xpath, key, deep):
        page = etree.HTML(data)
        for i in xpath:
            hrefs = page.xpath(u"//%s" % i) #根据xpath标签
            if deep >1:
                for href in hrefs:
                    url = href.attrib.get('href','')
                    if not url.startswith('java') and not url.startswith('#') and not \
                        url.startswith('mailto') and url.endswith('html'):  #过滤javascript和发送邮件的链接
                            self.tp.add_job(self.getPageSource,url, key, deep-1) #递归调用,直到符合的深
            for href in hrefs:
                value = href.text  #抓取相应标签的内容
                if value:
                    m = re.compile(r'.*%s.*' % key).match(value) #根据key匹配相应内容

    def work(self):
        self.tp.add_job(self.getPageSource, self.url, self.key, self.deep)
        self.tp.wait_for_complete() #等待线程池完成
