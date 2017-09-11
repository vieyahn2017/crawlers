import sys
import os
sys.path.append('../../django_scrapy_project_001')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'django_scrapy_project_001.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_scrapy_project_001.settings")


import django
django.setup()
