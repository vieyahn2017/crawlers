from __future__ import absolute_import,unicode_literals

from celery import Celery

app = Celery('SpiderCelery',
             broker='amqp://',
             include='OpenSpider.SpiderCelery.tasks')

app.conf.CELERY_RESULT_BACKEND =  'amqp://'

if __name__ == "__main__":
    app.start()