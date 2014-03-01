# -*- coding:utf-8 -*-

from rq2 import Queue,use_connection
from worker import conn
from pushworker import pushwork
from datetime import datetime
import pytz

use_connection(conn)
q = Queue()


#q.enqueue(pushwork2,'asd','1q2w3e')

import web
import model

from config import *

print datetime.now()

tz = pytz.timezone('GMT')
date = datetime.now(tz)
hour = date.hour
users =  model.get_current_push_users(hour)
if len(users) == 0:
	print '-=end=-'
else:
	#推送
	for user in users:
		feeds = []
		mfeeds = []
		feeds_num = 0
		ownfeeds = model.username2feeds(user.name)
		if len(ownfeeds) != 0:
			books = (model.get_allbooks())
			for book in books:
				if book.f_id in ownfeeds:
					b=[]
					if cmp('http',book.url[0:4].lower()) == 0:
						b.append(book.title)
						b.append(book.url)
						if book.isfulltext == 1:
							b.append(True)
						else:
							b.append(False)
						feeds.append(b)
					else:
						b.append(book.url)
						mfeeds.append(b)
					feeds_num += 1
			if user and user.kindle_email:
				q.enqueue(pushwork,args=(user.kindle_email,feeds,mfeeds,user.keep_image),timeout=feeds_num*300)
		print '-=end=-'
