__author__ = 'zhangxa'

from curl import Curl
from bs4 import BeautifulSoup

import pycurl

class Crawler:
    def __init__(self,url,*args,**kwargs):
        self.url = url
        self._url_lists = []
        self.initialize(*args,**kwargs)

    def initialize(self,*args,**kwargs):
        pass

    @property
    def url_lists(self):
        return self._url_lists

    def setUp(self):
        self.curl = Curl()

    def tearDown(self):
        self.curl.close()

    def grab(self):
        self.setUp()
        self.crawling()
        self.tearDown()

    def crawling(self):
        curl = self.curl
        curl.set_url(self.url)
        body = curl.get()
        print(body)

class Crawler_Jianshu(Crawler):
    def crawling(self):
        main_index = "http://www.jianshu.com"
        curl = self.curl
        curl.set_url(self.url)
        body = curl.get()
        bs = BeautifulSoup(body)
        a_tags = bs.find_all()
        for a_tag in a_tags:
            attrs = a_tag.attrs
            for attr in attrs:
                if attr in ('href','src','#src','#src2'): #find a url,some url likes javascript:void(null) are not filter
                    url = url_path = a_tag[attr]
                    if url_path.startswith("javascript"):
                        continue
                    if not url_path.startswith(main_index) and not url_path.startswith("http"):
                        url = main_index + url_path
                    self._url_lists.append(url)

class CrawlerDownHtml(Crawler):
    def initialize(self,*args,**kwargs):
        self.filname = kwargs['filename']

    def crawling(self):
        curl = Curl()
        curl.set_url(self.url)
        with open(self.filname,"wb") as output:
            curl.set_option(pycurl.WRITEFUNCTION,output.write)
            curl.get()
            curl.close()

if __name__ == "__main__":
    crawler = Crawler("www.jianshu.com")
    crawler.grab()