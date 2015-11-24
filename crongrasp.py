# -*- coding:utf-8 -*-

from rq2 import Queue,use_connection
from worker import conn
from pushworker import pushwork,pushwork2
import datetime
import time
import pytz
from books import FeedClasses, FeedClass
import os,re,urllib,urlparse,datetime,logging

use_connection(conn)
q = Queue()



import web
import model

from config import *

#计算时间差
def Caltime(date1,date2):
	date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
	date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
	date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
	date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
	return (date2-date1).seconds/3600

print '-------------------'
feeds = model.get_allbooks()

for feed in feeds:
	#是否需要更新
	if (feed.last_update == None) or (Caltime(feed.last_update.strftime("%Y-%m-%d %H:%M:%S"),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) >= feed.update_cycle):
	#更新
		temp_feed = []
		temp_f = []
		temp_f.append(feed.title)
		temp_f.append(feed.url)
		if feed.isfulltext == 1:
			temp_f.append(True)
		else:
			temp_f.append(False)
		temp_feed.append(temp_f)

		#用rq处理
		q.enqueue(pushwork2,args=(feed.f_id,temp_feed),timeout=300)

		print "-=end=-"
	else:
		#不用更新
		print 0
