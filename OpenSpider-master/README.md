# OpenSpider
一个python实现的开源爬虫

使用方法

1.首先在OpenSpider目录下，执行以下命令，以守护进程方式启动若干个worker

$ celery multi start worker1 worker2 worker3 -l info -A SpiderCelery

上面的命令启动了worker1,worker2,worker3共3个worker

2.启动爬虫主程序，开始爬行.

OpenSpider$ python main.py  
