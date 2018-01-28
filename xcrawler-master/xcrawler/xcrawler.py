# encoding: UTF-8
"""
    a light framework of crawler with gevent, requests, leveldb
    by veelion@ebuinfo.com
    Copyright © 2013 - 2014 Ebuinfo. All Rights Reserved.
"""
import sys
from gevent import monkey

if 'threading' in sys.modules:
    print 'gevent monkey patching all but threading...'
    monkey.patch_all(thread=False)
else:
    print 'gevent monkey patching all...'
    monkey.patch_all()

import gevent
from gevent import spawn
import gevent.queue
import requests
import time
import logging
import traceback


from proxypool import ProxyPool
from urlpool import UrlPool


RED = '\x1b[31m'
GRE = '\x1b[32m'
BRO = '\x1b[33m'
BLU = '\x1b[34m'
PUR = '\x1b[35m'
CYA = '\x1b[36m'
WHI = '\x1b[37m'
NOR = '\x1b[0m'


def init_file_logger(fname):
    # config logging
    from logging.handlers import TimedRotatingFileHandler
    ch = TimedRotatingFileHandler(fname, when="midnight")
    ch.setLevel(logging.INFO)
    # create formatter
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    # add formatter to ch
    ch.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    # add ch to logger
    logger.addHandler(ch)
    return logger


class XCrawler(object):
    '''index key-value: {url: state} , state:
        'task': the url is pending as a task
        'done': the url has been download seccessfully
    '''
    def __init__(self, max_working=20, common_gap=20,
                 urlindex_file="", proxies_file=None,
                 span_of_host=3,
                 max_in_mem=100000,
                 worker_conf_file='xworkers.conf',
                 load_bad_url=None, logfile=''):
        self.proxypool = ProxyPool(common_gap, proxies_file)
        self.urlpool = UrlPool(urlindex_file,
                               load_bad_url=load_bad_url,
                               span_of_host=span_of_host,
                               max_in_mem=max_in_mem,
                               is_good_link=self.is_good_link)
        self.max_working = max_working
        self.worker_conf_file = worker_conf_file
        self._workers = 0
        # you can customize your http header in init_urlpool()
        self.headers = None
        self._http_exception_code = 900
        if logfile:
            self.logger = init_file_logger(logfile)
        else:
            self.logger = logging.getLogger('xcrawler')
        self.failed_urls = {}

        # it is for hight priority url to download,
        # start() will get url from this queque firstly
        self.urlqueue = gevent.queue.Queue()

    def _worker(self, url):
        '''
            do a task
        '''
        try:
            self.logger.info('start a worker: [%s]' % self._workers)
            proxy, status_code, html, url_real = self.downloader(url)
            if not proxy and status_code == self._http_exception_code:
                status_code, html = self.special_downloader(url)
            if status_code == 200:
                new_urls = self.processor(url_real, html)
                self.urlpool.set_url_done(url)
                self.urlpool.set_url_done(url_real)
                if new_urls:
                    self.urlpool.addmany(new_urls)
            else:
                self.logger.info('%sfailed download: %s, [%s]%s' % (
                    RED,
                    url, status_code,
                    NOR,
                ))
                if proxy:
                    self.urlpool.set_url_404(url)
                    self.urlpool.add(url)
                elif (status_code == self._http_exception_code or
                      status_code >= 400):
                    # don't try more if no proxy
                    self.urlpool.set_url_bad(url)
                else:
                    t = self.failed_urls.get(url, 0)
                    if t == 0:
                        self.failed_urls[url] = 1
                        self.urlpool.add(url)
                    if t < 3:
                        self.failed_urls[url] += 1
                        self.urlpool.add(url)
                    if t >= 3:
                        self.urlpool.set_url_bad(url)
        except:
            traceback.print_exc()
        self._workers -= 1

    def dynamic_max_working(self,):
        changed = False
        try:
            ns = open(self.worker_conf_file).read()
            ns = int(ns)
            if ns != self.max_working:
                changed = True
                self.max_working = ns
            else:
                changed = False
        except:
            import os
            cmd = 'echo %s > %s' % (self.max_working, self.worker_conf_file)
            print '!!!!!! ', cmd
            os.system(cmd)
            pass
        if changed:
            msg = '%sset max_working to [%s]. %sworkers:[%s]%s' % (
                BRO,
                self.max_working,
                GRE,
                self._workers,
                NOR)
            print msg

    def start(self):
        self.init_urlpool()
        spawn(self.main_parallel_task_loop)
        self.dynamic_max_working()
        self.last_special_crawl = 0
        while 1:
            print '%sworkers left: %s%s' % (
                GRE,
                self._workers,
                NOR
            )
            self.dynamic_max_working()
            for i in xrange(self.max_working):
                if self._workers >= self.max_working:
                    gevent.sleep(10)
                    break
                try:
                    url = self.urlqueue.get_nowait()
                except:
                    url = self.urlpool.pop()
                gap = self.special_crawl_gap(url)
                skip_special = False
                if gap > 0:
                    to_sleep = gap - (time.time() - self.last_special_crawl)
                    if to_sleep > 0:
                        print '\tskip special:'
                        time.sleep(1)
                        self.urlpool.add(url, always=True)
                        skip_special = True
                    else:
                        self.last_special_crawl = time.time()
                if skip_special:
                    continue
                if not url:
                    break
                spawn(self._worker, url)
                self._workers += 1
            # wait for workers to start
            gevent.sleep(3)

    def main_parallel_task_loop(self,):
        '''define the task to do in a main-parallel loop'''
        return

    def special_crawl_gap(self, url):
        ''' re-define if sleep some time for this url
        '''
        return 0

    def is_ip_blocked(self, url, html):
        '''
        find ip blocked info in redirected url or html
        '''
        return False

    def is_good_link(self, url):
        '''
        filter url which you don't want to download
        re-implement if needs
        '''
        return True

    def init_urlpool(self, urls=None):
        '''
            init url pool with urls
            re-implement your own if need
        '''
        pass

    def special_downloader(self, url, timeout=20):
        ''' define supplementary to self.downloader()
        e.g. use special proxy to try in Exception in self.downloader()
        '''
        return (self._http_exception_code, '')

    def downloader(self, url, timeout=20):
        '''
            download url to get html
            re-implement your own if need
        '''
        if not self.headers:
            ua = ('Mozilla/5.0 (compatible; MSIE 9.0; '
                  'Windows NT 6.1; Win64; x64; Trident/5.0)')
            headers = {
                'User-Agent': ua,
            }
        else:
            headers = self.headers
        proxy, to_sleep = self.proxypool.get(url)
        if to_sleep > 10:
            print ('url: %s, proxy: %s ,to_sleep: %s' % (url, proxy, to_sleep))
        status_code = self._http_exception_code
        html = ''
        url_real = url
        try:
            msg = '%scrawl @[%s]-[%s]%s' % (BLU, time.ctime(), url, NOR)
            self.logger.debug(msg)
            if to_sleep:
                gevent.sleep(to_sleep)
            if proxy:
                timeout = 25
                r = requests.get(url, headers=headers,
                                 timeout=timeout, proxies=proxy)
            else:
                r = requests.get(url, headers=headers, timeout=timeout)
            html = r.content
            url_real = r.url.encode('utf8')  # get the redirected url
            status_code = r.status_code
            if self.is_ip_blocked(r.url, html):
                html = ''
                status_code = 400
                self.proxypool._pool.remove(proxy)
                print '%sremove proxy: %s, pool size: %s%s' % (
                    BRO, str(proxy), len(self.proxypool._pool), NOR)
        except:
            # traceback.print_exc()
            html = ''
        return (proxy, status_code, html, url_real)

    def processor(self, url, html):
        '''
            process the html from downloader
            e.g.
                extract URL, title, content and other info
                save the info extracted from html to DB
        '''
        new_urls = []
        return new_urls
