#!/usr/bin/python
#coding=utf-8

# Version 1 by Dongwm 2013/01/10
# 脚本作用：scrapy

from subprocess import call

def main():
	call('scrapy crawl localhost --nolog', shell=True)

if __name__ == '__main__':

    import timeit
    t = timeit.Timer("main()") 
    t.repeat(3, 10)
