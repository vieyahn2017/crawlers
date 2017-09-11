from scrapy import Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import sys
import datetime

#log_name=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#sys.stdout=open('stacks____%s.log'%log_name ,'w')

#import time
#time.strftime("%H:%M:%S")

#class StackCrawlerSpider(CrawlSpider): 
class StackCrawlerSpider(Spider): 
	name="stacks"
	allowed_domains=["51cto.com/",]

	start_urls=["http://bigdata.51cto.com/",]
	# 2017发现这个页面改成瀑布流了，正好可以研究这个怎么爬。TODO

	"""
	rules =(Rule(LinkExtractor(allow=r'col/577/list_577_[1-9].htm'),
		callback='parse_item', follow=True), )
	"""

	def parse(self, response):
	#def parse_item(self, response):
		yield scrapy.Request(
			url = self.domain,
			headers = self.headers,
			meta = {'proxy': UsersConfig['proxy'],  'cookiejar': 1 },
			callback = self.parse_items,
			dont_filter=True
			)


	def parse_items(self, response):
		pass

