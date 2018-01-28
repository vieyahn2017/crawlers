xcrawler
========

a light framework of crawler with gevent, requests, leveldb

Features
========
1. multiple crawling task, use coroutine of gevent;
2. a url pool to manage urls (downloaded or to download), use leveldb;
3. a proxy pool to avoid blocked by the site while quering very frequently;

Installation
========
sudo python setup.py install


Usage
========
Sorry for no docs right now, just see the [example](https://github.com/veelion/xcrawler/blob/master/example/site_crawler.py) or read the [source code](https://github.com/veelion/xcrawler/blob/master/xcrawler/xcrawler.py)
