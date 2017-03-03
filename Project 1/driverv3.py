
from Queue import Queue

def makeNeighbours(parent):
	zIndex = parent.index(0)

	x = parent[zIndex]
	
	neighbours = []
	direction = []
	if zIndex > 2: # list for 'up'
		child = list(parent) # use this to clone a list, not child = parent (which changes parent every time child changes)
		y = parent[zIndex-3]
		child[zIndex] = y
		child[zIndex-3] = x
		neighbours.append(child)
		direction.append('up')

	if zIndex <6: # list for down
		child = list(parent)
		y = parent[zIndex+3]
		child[zIndex] = y
		child[zIndex+3] = x
		neighbours.append(child)
		direction.append('down')
	if zIndex%3 != 0: # 'left'
		child = list(parent)
		y = parent[zIndex-1]
		child[zIndex]=y
		child[zIndex-1]=x
		neighbours.append(child)
		direction.append('left')

	if zIndex%3 != 2: # 'right'
		child = list(parent)
		y = parent[zIndex+1]
		child[zIndex]=y
		child[zIndex+1]=x
		neighbours.append(child)
		direction.append('right')
	return neighbours,direction

class state(list):

    def __init__(self, parentState):
    	self.parentState = parentState
    	neighbours,direction = makeNeighbours(parentState)
    	self.neighbours = neighbours
    	self.direction = direction

def driverTest(initialState):

	frontier = Queue(maxsize=0)
#	direction = Queue(maxsize=0)
#	x = state(initialState)
	frontier.put(initialState)
	explored=[]
	exploredDir = []
	while not frontier.empty():
		currentList =  frontier.get()
		frontier.task_done()
		print currentList
		currentState = state(currentList)
		explored.append(currentList)
		exploredDir.append(currentState.direction)
		print exploredDir


		if currentList == [0,1,2,3,4,5,6,7,8]:
			return True

		else:
			if currentState.neighbours:
				for neighbour in currentState.neighbours:
					if neighbour not in frontier.queue:
						if neighbour not in explored:  # nested if statements used because 'or'ing them together was not working as expected
							frontier.put(neighbour)


x = driverTest([1,2,5,3,4,0,6,7,8])



