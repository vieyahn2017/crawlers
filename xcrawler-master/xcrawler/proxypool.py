#encoding: UTF-8
"""
    select a proxy for url according its host from proxy pool
    by veelion@ebuinfo.com
    Copyright © 2013 - 2014 Ebuinfo. All Rights Reserved.
"""

import urlparse
import time
import random
import re


class ProxyPool(object):
    '''
    to get a proxy from pool for url whith different host each time
    '''
    def __init__(self, common_gap=15, proxies_file=''):
        self._proxy_file = proxies_file
        self._pool = []  # list of proxy dicts loading from proxy_file
        self.load(proxies_file)
        self._common_gap = common_gap
        self._special_gap = {} # {host:gap}
        self._host_proxy_time = {} # {host: [[index_of_pool, last_use_time] * len(self._pool)]}, `pool_index` indicates the proxy in the pool,  `last_use_time` record the time accessing `host`
        self._host_last_proxy_id = {} # {host: last_proxy_index}, `last_proxy_index` indicates the proxies in the pool used to access `host`s last time.
        self._proxy_failed = {} # {proxy: failed_count}
        self._proxy_failed_threshold = 7
        self.FAILED = 0
        self.SUCCESS = 1

        # for no proxy
        self._host_last_time = {} # {host: last_access_time}

    def load(self, proxies_file):
        '''
        each line has two items split by space in proxies_file which like:
            http http://10.10.1.10:3128
            https http://user:password@10.10.1.10:3128,

        self._pool is a list of proxy
        whose format is compatible with python-requests:
            proxy = {
            "http": "http://user:password@10.10.1.10:3128",
            "https": "http://10.10.1.10:1080",
            }
        '''
        try:
            lines = open(proxies_file).readlines()
        except:
            lines = []

        for l in lines:
            if l.startswith('#'): continue
            ii = re.split(r'\s+', l.strip())
            if len(ii) != 2:
                print 'invalid proxy line: ', l
                continue
            proxy = {
                ii[0]: ii[1],
            }
            self._pool.append(proxy)
        print 'there are [%s] proxies in the ProxyPool' % len(self._pool)

    def set_host_gap(self, host, gap):
        self._special_gap[host] = gap

    def record_proxy_state(self, proxy, state):
        if not proxy: return
        proxy_url = proxy['http']
        if state == self.FAILED:
            if proxy_url in self._proxy_failed:
                self._proxy_failed[proxy_url] += 1
                if self._proxy_failed[proxy_url] > self._proxy_failed_threshold:
                    try:
                        print '!!! remove proxy: %s , left: [%s] !!!' % (
                            proxy_url,
                            len(self._pool)
                        )
                        # TODO proxy pool changed, changes should also be made to recording data structures such as _host_proxy_time
                        self._pool.remove(proxy)
                    except:
                        pass
            else:
                self._proxy_failed[proxy_url] = 1
        elif state == self.SUCCESS:
            if proxy_url in self._proxy_failed:
                if self._proxy_failed[proxy_url] > 0:
                    self._proxy_failed[proxy_url] -= 1
        else:
            print '!!!!! invalid proxy state: %s !!!!' % state

    def get(self, url):
        ''' return (proxy, to_sleep_time)'''
        host = urlparse.urlparse(url).netloc
        proxy = None
        to_sleep = 0
        now = int(time.time())
        if self._pool:
            index = -1
            if host in self._host_last_proxy_id:
                index = self._host_last_proxy_id[host] + 1
                index %= len(self._pool)
                self._host_last_proxy_id[host] = index
                passed = now - self._host_proxy_time[host][index][1]
                if host in self._special_gap:
                    to_sleep = self._special_gap[host] - passed
                else:
                    to_sleep = self._common_gap - passed
                if to_sleep < 0:
                    to_sleep = 0
                self._host_proxy_time[host][index][1] = now + to_sleep
            else:
                # init this host for each proxy
                proxy_times = []
                for idx in xrange(len(self._pool)):
                    proxy_times.append([idx,0])
                # proxy_times = [[idx, 0] for idx in xrange(len(self._pool))]
                index = random.randint(0, len(self._pool)-1)
                proxy_times[index][1] = now
                self._host_proxy_time[host] = proxy_times
                self._host_last_proxy_id[host] = index
            proxy = self._pool[index]
        else:
            # no proxy, just return to_sleep time
            to_sleep = 0
            if host in self._host_last_time:
                passed = now - self._host_last_time[host]
                if host in self._special_gap:
                    to_sleep = self._special_gap[host] - passed
                else:
                    to_sleep = self._common_gap - passed
                if to_sleep < 0:
                    to_sleep = 0
            self._host_last_time[host] = now + to_sleep
        return (proxy, to_sleep)

if __name__ == '__main__':
    urls = [
        'http://baidu.com/1.html',
        'http://baidu.com/2.html',
        'http://baidu.com/3.html',
        'http://baidu.com/4.html',
        'http://baidu.com/5.html',
        'http://baidu.com/6.html',
        'http://baidu.com/7.html',
        'http://baidu.com/8.html',
        'http://baidu.com/9.html',
        'http://baidu.com/1.html',
        'http://baidu.com/1.html',
        'http://baidu.com/2.html',
        'http://baidu.com/1.html',
        'http://baidu.com/1.html',
        'http://baidu.com/1.html',
        'http://baidu.com/1.html',
    ]

    pp = ProxyPool(30, proxies_file='proxies.list.small.z')

    def test(url):
        proxy, to_sleep = pp.get(url)
        print url
        print proxy, ' : ', to_sleep
        print '\n'

    import gevent
    gthreads = [gevent.spawn(test, url) for url in urls]
    start = time.time()
    gevent.joinall(gthreads)
    finish = time.time()

    print 'it takes %.6f seconds' % (finish - start)
    #from gevent.pool import Pool
    #gpool = Pool(100)
    #gpool.map(test, urls)
    #gpool.join()
