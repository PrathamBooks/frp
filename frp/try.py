import os
from frp.service.image_backup import save_image
from rq import Queue
from rq.job import Job
import redis

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)
q = Queue(connection=conn)

new_file_name = '10.jpg'
job = q.enqueue_call(
  func=save_image, 
  args=(os.path.join("/home/infodigital/frp/frp/frp/static/uploads", 'uploads'),
    new_file_name,), 
    result_ttl=5000
    )
print ('image save job id: ' + str(job.id))


