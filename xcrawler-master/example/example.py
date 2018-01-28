#!/usr/bin/env python
#encoding: utf8

from xcrawler import XCrawler

import lxml.html
import logging
import urlparse

class MyCrawler(XCrawler):
    def init_urlpool(self,):
        urls = [
            'http://news.163.com',
        ]
        self.urlpool.addmany(urls)


    def processor(self, url, html):
        if not html:
            return []
        try:
            et = lxml.html.fromstring(html, base_url=url)
        except Exception, e:
            print e
            return []
        title = et.xpath('//title')
        for i in title:
            t = i.text.strip()
            print t, url
        links = []
        aa = et.xpath('//a')
        if not aa:
            return links
        for a in aa:
            h = a.get('href', '')
            if not h:
                continue
            if not h.startswith('http') or 'news.163.com' not in h:
                continue
            u = urlparse.urljoin(url, h)
            links.append(u)
        self.logger.debug('new links: %s' % len(links))
        return links


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    proxies = [
        'http://27.24.158.131/',
        'http://27.24.158.131/',
        'http://58.20.223.230/',
        'http://27.24.158.130/',
        'http://27.24.158.130/',
        'http://27.24.158.155/',
        'http://202.98.123.126/',
        'http://27.24.158.155/',
        'http://114.141.162.53/',
        'http://50.57.231.130/',
        'http://211.167.64.112/',
    ]
    mc = MyCrawler(max_working=3, logfile='xcrawler.log') ## gen_task() will be called
    mc.start()


