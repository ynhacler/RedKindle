# -*- coding:utf-8 -*-
#test
import os,re,urllib,urlparse,datetime,logging
from datetime import date, timedelta
from config import *
from books.base import BaseFeedBook,  BaseUrlBook,WebpageBook
from jinja2 import Environment, PackageLoader
from os import path, listdir, system
from shutil import copy,copytree
#from books.ZhihuDaily import ZhihuDaily
from books import FeedClasses, FeedClass

log = logging.getLogger()

#zzh = ZhihuDaily(log)

#url=zzh.ParseFeedUrls()

#print url

feedsclasses =  FeedClasses()

for feed in feedsclasses:
#zzh = feed(log)
#	url = zzh.ParseFeedUrls()
#	print url
#	print '================='
	if feed.__name__ == 'DoubanBook':
		print 1

