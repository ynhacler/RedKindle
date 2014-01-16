import os,redis
from pushworker import pushwork
from rq import Queue,Worker,Connection,use_connection

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

use_connection(conn)
q = Queue()


print os.path.split(os.path.realpath(__file__))[0]
q.enqueue(pushwork,'asd','1q2w3e')
