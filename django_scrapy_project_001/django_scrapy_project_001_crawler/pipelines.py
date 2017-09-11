# -*- coding: utf-8 -*-

#import pymongo
from pymongo import MongoClient
import psycopg2
from scrapy.conf import settings
from scrapy.exceptions import DropItem

import re
import urllib

"""
import sys
import datetime
reload(sys) 
sys.setdefaultencoding( "utf-8" )
log_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sys.stdout=open(r'pipe____%s.log'%log_time ,'w')
"""

class DjangoPipeline(object):

	def __init__(self):
		self.counter = 0

	def process_item(self, item, spider):
		self.counter += 1
		print self.counter, '\n------pipe this----:', item
		try:
			item.save()
		except Exception, e:
			print "Error: %s" % e
		return item



class PostgresPipeline(object):

	def __init__(self):
		self.counter=0
		self.connection = psycopg2.connect(
			database=settings['POSTGRES_DB'],
			user=settings['POSTGRES_USER'],
			password=settings['POSTGRES_PW'],
			host=settings['POSTGRES_SERVER'],
			port=settings['POSTGRES_PORT'],
		)
		self.cursor = self.connection.cursor()


	def process_item(self, item, spider):
		self.counter += 1 
		print self.counter, ' ------pipe this----:', item
		try:
			_pre_sql = """INSERT INTO article(url, title, publish_time, brows, abstract, image) 
						VALUES('%s', '%s', '%s', %s, '%s', '%s');""" % (item['url'], item['title'], item['publish_time'], item['brows'], item['abstract'], item['image'])  
			insert_sql = self.cursor.mogrify(_t)
			print insert_sql
			self.cursor.execute(insert_sql)
			self.connection.commit()
		except Exception, e:
			print "Error: %s" % e

		return item


class MongoDBPipeline(object):
	def __init__(self):
		connection = MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		valid = True
		for data in  item:
			if not data:
				valid=False;
				raise DropItem("Missing {0}!".format(data))
		if valid:
			self.collection.insert(dict(item))
			#log.msg("Article added to MongoDB database!",level=log.DEBUG, spider=spider)

		return item

