from scrapy import Spider
from scrapy.selector import Selector
from django_scrapy_project_001_crawler.items import StackDjangoItem, StackItem
import datetime
import re
import urllib


class StackSpider(Spider):
	name = "stack"
	allowed_domains = ["http://bigdata.51cto.com/"]

	#start_urls = ["http://bigdata.51cto.com/",]
	start_urls = []
	for i in range(1, 11): # 暂时只爬10页
		start_urls.append("http://bigdata.51cto.com/col/577/list_577_%s.htm" %i)

	def parse(self, response):	
		try:
			articles = Selector(response).xpath('//div[@class="list_leftcont"]')
			for arc in articles:
				item = StackDjangoItem()
				#item = StackItem()
				item['title'] = arc.xpath('div/div[@class="list_leftcont01"]/h4/a/text()').extract()[0]
				item['url'] = arc.xpath('div/div[@class="list_leftcont01"]/h4/a/@href').extract()[0]
				image= arc.xpath('div/div[@class="list_pic"]/a/img/@src').extract()[0]
				item['publish_time'] = arc.xpath('div/div[@class="list_leftcont01"]/p[@class="timeline"]/span[1]/text()').extract()[0]
				item['brows'] = filter(lambda x:x.isdigit(),
					arc.xpath('div/div[@class="list_leftcont01"]/p[@class="timeline"]/span[2]/text()').extract()[0]) 
				item['abstract'] = arc.xpath('div/div[@class="list_leftcont01"]/p[@class="list_info01"]/text()').extract()[0]
				item['label'] = arc.xpath('div[@class="tagbox"]/p[@class="tag_info"]/a/text()').extract()
				
				rstr = r"[\/\\\:\*\?\"\<\>\|]"      # '/\:*?"<>|'
				new_title = re.sub(rstr, "", item['title'])
				t_url = item['url'].split('/')
				image_file = t_url[-2] + '__' + t_url[-1] + '__' + new_title + '.jpg'
				urllib.urlretrieve(image, "img/%s" %image_file)
				item['image'] = image
				item['image_file'] = image_file
				item['tmp'] = datetime.datetime.now()
				print ' \n ------stack and parse    this----:   '
				print item, '\n'
				yield item

		except Exception, e:
			print "Error: %s" % e

