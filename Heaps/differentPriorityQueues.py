import Queue as Q

q = Q.PriorityQueue()
q.put(20)
q.put(45)
q.put(32)
while not q.empty():
	print q.get() # outputs smallest element first


""" example with tuples """
import Queue as Q  # ver. < 3.0
# import queue as Q  # otherwise

q = Q.PriorityQueue()
q.put((10,'ten'))
q.put((1,'one'))
q.put((5,'five'))
while not q.empty():
    print q.get()


""" example with class objects """
# try and except are used for error handling. Video explanation link: https://www.youtube.com/watch?v=NIWwJbo-9_8
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

class Skill(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print 'New Level:', description
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

q = Q.PriorityQueue()

q.put(Skill(5, 'Proficient'))
q.put(Skill(10, 'Expert'))
q.put(Skill(1, 'Novice'))

while not q.empty():
    next_level = q.get()
    print 'Processing level:', next_level.description

""" Example with heaps """
import heapq

heap = []
heapq.heappush(heap, (1, 'one'))
heapq.heappush(heap, (10, 'ten'))
heapq.heappush(heap, (5,'five'))

for x in heap:
	print x,
print

heapq.heappop(heap)

for x in heap:
	print x,
print 

# the smallest
print heap[0]
