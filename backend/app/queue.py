import os
from redis import Redis
from rq import Queue
REDIS_URL=os.getenv("REDIS_URL","redis://redis:6379/0")
redis_conn=Redis.from_url(REDIS_URL,socket_connect_timeout=3,socket_timeout=5)
queue=Queue("job-scrapes",connection=redis_conn,default_timeout=900)
