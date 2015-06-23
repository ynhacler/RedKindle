# -*- coding:utf-8 -*-

#监听任务队列并处理

import os,redis
from rq2 import Worker,Queue,Connection

listen = ['high','default','low']

redis_url = os.getenv('REDISTOGO_URL','redis://localhost:6379')

conn = redis.from_url(redis_url)


if __name__ == '__main__':
	with Connection(conn):
		worker = Worker(map(Queue,listen))
		worker.work()
