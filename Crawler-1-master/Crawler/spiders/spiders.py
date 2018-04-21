from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item

class MySpider(CrawlSpider):
    name = 'localhost'
    allowed_domains = ['localhost']
    start_urls = ['http://localhost']
    rules = ( 
        Rule(SgmlLinkExtractor(allow=(r'http://localhost/.*')), callback="parse_item"),  
    )  
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        hxs.select('//*[@*]/text()').re(r'py')
