
from Queue import Queue

def move(parent,dir):
	zIndex = parent.index(0)

	x = parent[zIndex]
	child = list(parent) # use this to clone a list, not child = parent (which changes parent every time child changes)
	if dir == 'up':
		if zIndex > 2:
			y = parent[zIndex-3]
			child[zIndex] = y
			child[zIndex-3] = x
		else:
			child = []
	elif dir == 'down':
		if zIndex <6:
			y = parent[zIndex+3]
			child[zIndex] = y
			child[zIndex+3] = x
		else:
			child = []
	elif dir == 'left':
		if zIndex%3 == 0:
			child = []
		else:
			y = parent[zIndex-1]
			child[zIndex]=y
			child[zIndex-1]=x
	elif dir == 'right':
		if zIndex%3 == 2:
			child = []
		else:
			y = parent[zIndex+1]
			child[zIndex]=y
			child[zIndex+1]=x
	return child

class state(list):

    def __init__(self, parentState):
    	self.parentState = parentState
    	if parentState:
    		self.childUp = move(self.parentState,'up')
    		self.childDown = move(self.parentState,'down')
    		self.childLeft = move(self.parentState,'left')
    		self.childRight = move(self.parentState,'right')
    		self.neighbours = [self.childUp,self.childDown,self.childRight,self.childLeft]
    	else:
    		self.neighbours= []

def driverTest(initialState):

	frontier = Queue(maxsize=0)
	x = state(initialState)
	frontier.put(x.parentState)

	explored = set()
	print x.parentState
	while not frontier.empty():
		currentList =  frontier.get()
		frontier.task_done()

		print currentList
		currentState = state(currentList)
		currenTupl = tuple(currentList)
		explored.add(currenTupl)


		if currentList == [0,1,2,3,4,5,6,7,8]:
			return True

		else:
			if currentState.neighbours:
				for neighbour in currentState.neighbours:
					if neighbour not in frontier.queue or tuple(neighbour) not in explored:
						frontier.put(neighbour)


x = driverTest([1,2,3,4,5,0,8,6,7])



