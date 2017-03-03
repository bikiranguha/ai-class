from Queue import Queue

def do_stuff(q):
  while not q.empty():
    print q.get() # prints the next item in queue, in FIFO fashion
    q.task_done() # need to call after 

q = Queue(maxsize=0)

for x in range(20):
  q.put(x)

do_stuff(q)