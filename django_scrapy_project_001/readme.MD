#1.用Django命令新建项目：
django-admin startproject django_scrapy_project_001

#2.配置settings 里面的db
 用django以后，不用自己写数据库各种接口，只需要在这边配置db即可   
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scrapy',
        'USER': 'test',
        'PASSWORD': 'test',
        'HOST': '',
        'PORT': '',
    }
}
```

#3.用Django命令新建App
cd django_scrapy_project_001   
django-admin startapp django_scrapy_project_001_app_01   

#4.把新建的App加入工程当中：
在settings的INSTALLED_APPS加入：   
django_scrapy_project_001_app_01

#5.为App写Model
```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now

class Article(models.Model):
    url = models.URLField('网页地址', max_length=200, null=True)
    title = models.CharField('标题', max_length=100)
    publish_time = models.DateTimeField('发布时间', default=now, null=True)
    brows = models.IntegerField('浏览量', default=0, null=True)
    abstract = models.TextField('摘要', default=now, null=True)
    label = ArrayField(models.CharField('标签', max_length=20), null=True)
    image = models.URLField('图片路径', null=True)
    image_file = models.FilePathField('图片地址', path=None, null=True)
    tmp = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.title

class Meta:
    ordering = ['-brows']
```

#6.将Model导入数据库
python manage.py makemigrations django_scrapy_project_001_app_01   
python manage.py sqlmigrate django_scrapy_project_001_app_01 0001   
python manage.py migrate   
这样直接导入即可

#7.新建Scrapy项目
然后在这个目录建scrapy的工程   
scrapy startproject django_scrapy_project_001_crawler   
这样的目录层级多一层，不太好   
直接把里面的文件全部复制到外面一层，让scrapy.cfg跟django的manage.py在同一级  


#8.调整scrapy项目：
修改settings的各个配置   

复制来   
pipelines.py和middlewares.py   
（这两文件多数都不用改的）   

#9.将django的project要加入到scrapy中来：
在scrapy下面的init.py添加：
```python
import sys
import os
sys.path.append('../../django_scrapy_project_001')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'django_scrapy_project_001.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_scrapy_project_001.settings")

import django
django.setup()
```

#10.书写爬虫模块
scrapy基本上架构都不需要怎么改，   
主要是爬取模块./spiders
```python
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


```

#11.scrapy爬取
scrapy crawl stack   
等数据爬取下来

#12.可视化
去django的app中，
修改views以及templates
```python
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.http import HttpResponse, Http404
from django_scrapy_project_001_app_01.models import *

def list_all(request):
    #return HttpResponse("List all")
    articles = Article.objects.all()[:7] #测试只用7个元素
    return render_to_response('1.htm', {'articles':articles})
```
模板：
```html
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>
<ul>
{% for item in articles %}
<li>
<div class="ztitle">'标题',{{ item.title }} </div>
<div>'浏览量' {{ item.brows }} </div>
<div>'发布时间' {{ item.newstime}} </div>
<div>'网页地址' {{ item.url }} </div>
<div>'标签':
{% for item_l in item.label  %}
 <span>{{ item_l  }} </span>
{% endfor %}
 </div>
<div>'摘要' {{ item.abstract}} </div>
<div class="zimage">'图片网址'<img  src={{ item.image }} class="img200"> </div>
<div>'图片路径' {{ item.image_file}} </div>
<p>
</li>
{% endfor %}
</ul>
</body>
</html>

```
#13.导入app的视图
将app的views的方法加入project的urls中
```python
from django.conf.urls import url
from django.contrib import admin
from django_scrapy_project_001_app_01.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lists/$', list_all),
    url(r'^$', list_all),
    url(r'^hello/$', hello),
]
```

#14.运行django
python manage.py runserver   

运行即可查看效果   
http://127.0.0.1:8000/