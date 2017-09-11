# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.http import HttpResponse, Http404
from django_scrapy_project_001_app_01.models import *

def list_all(request):
	#return HttpResponse("List all")
	articles = Article.objects.all()[:7] #测试只用7个元素
	return render_to_response('1.htm', {'articles':articles})

def hello(request):
	return  HttpResponse("hello django_scrapy_project!")
