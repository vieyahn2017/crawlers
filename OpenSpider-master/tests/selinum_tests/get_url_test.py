__author__ = 'zhangxa'

import unittest

from selenium import webdriver
from bs4 import BeautifulSoup

class Get_Url_Test(unittest.TestCase):
    def test_PhantomJS_get(self):
        url = 'http://www.lagou.com/'
        driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
        driver.get(url)
        pagesource = driver.page_source
        bs = BeautifulSoup(pagesource)
        url_lists = []
        a_tags = bs.findAll()
        for a_tag in a_tags:
            attrs = a_tag.attrs
            for attr in attrs:
                if attr in ('href','src','#src','#src2'): #find a url,some url likes javascript:void(null) are not filter
                    url = url_path = a_tag[attr]
                    if url_path.startswith("/"):
                        url_path = "http:"+url_path
                    if url_path.startswith("http:"):
                        url_lists.append(url_path)
        print(url_lists)
        self.assertIsNotNone(pagesource)

    def test_PhantomJS_login(self):
        url = 'https://passport.lagou.com/login/login.html'
        driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
        driver.get(url)
        pagesource = driver.page_source
        print(pagesource)
        bs = BeautifulSoup(pagesource)
        with open('1.html','wb') as f:
            f.write(pagesource)
        self.assertIsNone(bs)

if __name__ == "__main__":
    unittest.main(warnings='ignore')

