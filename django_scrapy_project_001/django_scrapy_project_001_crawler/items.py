# -*- coding: utf-8 -*-

from scrapy import Item, Field
from django_scrapy_project_001_app_01.models import Article

from scrapy_djangoitem import DjangoItem

class StackDjangoItem(DjangoItem):
	""" for DjangoPipeline. """
	django_model = Article



class StackItem(Item):
	""" for PostgresPipeline. """
	url = Field()
	title = Field()
	publish_time = Field()
	brows = Field()
	abstract = Field()
	label = Field()
	image = Field()
	image_file = Field()

