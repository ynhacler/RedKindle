
from rq2 import Queue,use_connection
from worker import conn
from pushworker import pushwork2
use_connection(conn)
q = Queue()


q.enqueue(pushwork2,'asd','1q2w3e')
