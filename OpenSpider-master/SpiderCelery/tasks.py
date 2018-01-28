from __future__ import absolute_import,unicode_literals

from OpenSpider.SpiderCelery.celery import app
from OpenSpider.crawler import Crawler_Jianshu
from bs4 import BeautifulSoup
from selenium import webdriver

PHANTOMJS_PATH='/usr/bin/phantomjs'

@app.task
def fetch_a_url(url):
    try:
        driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
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
        return url_lists
    except Exception as e:
        print("fetch error",e)

@app.task
def jianshu_crawler(url):
    try:
        crawler = Crawler_Jianshu(url)
        crawler.grab()
        return crawler.url_lists
    except Exception as e:
        print("jianshu_crawler exception",e)