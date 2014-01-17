# -*- coding:utf-8 -*-

from rq2 import Queue,use_connection
from worker import conn
from pushworker import pushwork2
from datetime import datetime
import pytz

use_connection(conn)
q = Queue()


#q.enqueue(pushwork2,'asd','1q2w3e')

import web
import model

from config import *


if __name__ == "__main__":
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
			ownfeeds = model.username2feeds(user.name)
			if len(ownfeeds) != 0:
				books = (model.get_allbooks())
				for book in books:
					if book.f_id in ownfeeds:
						b=[]
						b.append(book.title)
						b.append(book.url)
						feeds.append(b)
				if user and user.kindle_email:
					q.enqueue(pushwork,user.kindle_email,feeds)

		print '-=end=-'

