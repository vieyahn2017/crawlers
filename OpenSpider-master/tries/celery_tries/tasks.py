__author__ = 'zhangxa'

from celery import Celery
from selenium import webdriver
from bs4 import BeautifulSoup

import time

app = Celery('tasks',broker='amqp://')

app.conf.CELERY_RESULT_BACKEND =  'amqp://'


@app.task
def add(x,y):
    return x + y

@app.task
def sleep(seconds):
    time.sleep(float(seconds))
    return seconds

@app.task
def fetch_a_url(url):
    try:
        driver = webdriver.PhantomJS(executable_path="/usr/bin/phantomjs")
        driver.get(url)
        pagesource = driver.page_source
        bs = BeautifulSoup(pagesource)
        url_lists = []
        a_tags = bs.find_all()
        for a_tag in a_tags:
            attrs = a_tag.attrs
            for attr in attrs:
                if attr in ('href','src','#src','#src2'): #find a url,some url likes javascript:void(null) are not filter
                    url = url_path = a_tag[attr]
                    if url_path.startswith("//"):
                        url_path = "http:"+url_path
                    if url_path.startswith("http:"):
                        url_lists.append(url_path)
        return url_lists
    except Exception as e:
        print("fetch error",e)

if __name__ == "__main__":
    app.start()
