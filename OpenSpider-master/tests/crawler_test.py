__author__ = 'zhangxa'

from OpenSpider.crawler import CrawlerDownHtml,Crawler_Jianshu

import unittest
import os

class CrawlerDownHtml_test(unittest.TestCase):
    def test_DownHtml(self):
        crawler = CrawlerDownHtml("www.jianshu.com",filename="index.html")
        crawler.grab()
        self.assertTrue(os.path.exists("index.html"))

class CrawlerJianshu_test(unittest.TestCase):
    def test_Jianshu(self):
        crawler = Crawler_Jianshu("www.jianshu.com")
        crawler.grab()
        print(crawler.url_lists)
        self.assertIsNotNone(crawler.url_lists)

if __name__ == "__main__":
    unittest.main(warnings='ignore')