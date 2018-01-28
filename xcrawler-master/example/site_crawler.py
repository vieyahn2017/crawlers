#!/usr/bin/env python
#encoding: utf8

from xcrawler import XCrawler, encoding
import xcrawler
import gevent

import logging
import urlparse
import traceback
import lxml.html


class SiteCrawler(XCrawler):
    def get_hub_urls(self,):
        '''re-define this function if you want to get a certain urls'''
        ## load hub urls from db
        urls = [
            'http://news.163.com/',
            'http://news.sina.com.cn',
        ]
        self.hub_urls = {} # {url: download_failure_count}
        self.hub_hosts = set()
        for url in urls:
            self.hub_urls[url] = 0
            pr = urlparse.urlparse(url)
            host = pr.netloc
            self.hub_hosts.add(host)
        print 'load hub urls: ', len(self.hub_urls)

    def init_urlpool(self,):
        self.get_hub_urls()
        if not self.hub_urls:
            print 'no hub urls loaded, plz set hub urls you want to crawl first'
            import sys
            sys.exit(-1)

    def main_parallel_task_loop(self,):
        print '%smain-parallel-loop starting...%s' % (
            xcrawler.GRE,
            xcrawler.NOR,
        )
        span = 30 #seconds
        while 1:
            for hub in self.hub_urls:
                proxy,code,html,url_real = self.downloader(hub)
                if not proxy and code == self._http_exception_code:
                    code, html = self.special_downloader(hub)
                    self.hub_urls[hub] = 0
                if code == 200:
                    newlinks = self.extract_links(hub, html)
                    self.urlpool.addmany(newlinks)
                else:
                    print 'failed downloading: %s, [%s]' % (hub, code)
                    self.hub_urls[hub] += 1
                    if self.hub_urls[hub] > 10:
                        msg = '%sfiled downloading [%s] for more than [%s] times%s' % (
                            xcrawler.RED,
                            hub,
                            10,
                            xcrawler.NOR)
                        print msg
            gevent.sleep(span)

    def fix_news_url(self, url):
        news_postfix = [
            '.html?', '.htm?', '.shtml?',
            '.shtm?',
        ]
        p = url.find('#')
        if p > -1:
            url = url[:p]
        for np in news_postfix:
            p = url.find(np)
            if p > -1:
                p = url.find('?')
                url = url[:p]
                break
        return url

    def is_good_link(self, url):
        if '&' in url:
            return False
        bad_postfix = set([
            'exe', 'doc', 'docx', 'xls', 'xlsx',
            'jpg', 'png', 'bmp', 'jpeg',
            'zip', 'rar', 'tar', 'bz2', '7z',
            'flv', 'mp4',
        ])
        postfix = url.split('.')[-1]
        if postfix in bad_postfix:
            return False
        is_good = False
        pr = urlparse.urlparse(url)
        link_host = pr.netloc
        if link_host in self.hub_hosts:
            is_good = True
        return is_good

    def extract_links(self, url, html):
        if not html: return []
        if not isinstance(html, unicode):
            enc, html = encoding.html_to_unicode('', html)
        try:
            doc = lxml.html.fromstring(html, base_url=url)
        except:
            print traceback.print_exc()
            return []
        doc.make_links_absolute()
        el_a = doc.xpath('//a')
        newlinks = []
        if not el_a:
            return newlinks
        for a in el_a:
            link = a.get('href', '')
            if not link: continue
            if not self.is_good_link(link):
                continue
            link = self.fix_news_url(link)
            newlinks.append(link)
        newlinks = list(set(newlinks))
        return newlinks

    def save_html(self, url, html):
        '''return True if saved successfully
            save url, html in your Database
        '''
        succeed = True
        return succeed

    def processor(self, url, html):
        links = []
        if not html or len(html) < 2000:
            return links
        if not self.save_html(url, html):
            links.append(url)
        ## extract news url from a baidu news page
        links.extend(self.extract_links(url, html))
        return links


if __name__ == '__main__':
    import time
    logging.basicConfig(level=logging.ERROR)
    sc = SiteCrawler(
        max_working=400,
        common_gap=0,
        urlindex_file = 'url.index-%s' % __file__.split('/')[-1],
        #load_bad_url = True,
        #proxies_file='proxy.list',
    )
    pause = 1
    print 'will start crawling in [%s] seconds' % pause
    time.sleep(pause)
    sc.start()





