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