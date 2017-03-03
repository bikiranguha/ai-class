
from Queue import Queue
import time
#import resource # uncomment when running in linux
start_time = time.clock()


class neighbours(object):

	def __init__(self):
		self.List = []  # Stores a list of neighbours of the current state
		self.ID = []  # ID stores the direction from the root node of the current state

def makeNeighbours(parent,parentID):
	zIndex = parent.index(0)

	x = parent[zIndex]
	
	nbr = neighbours()



	if zIndex > 2: # list for 'up'
		child = list(parent) # use this to clone a list, not child = parent (which changes parent every time child changes)
		y = parent[zIndex-3]
		child[zIndex] = y
		child[zIndex-3] = x
		if parentID == 'root':
			childID = []
		else:
			childID = list(parentID)
		childID.append('up')
		nbr.List.append(child)
		nbr.ID.append(childID)




	if zIndex <6: # list for down
		child = list(parent)
		y = parent[zIndex+3]
		child[zIndex] = y
		child[zIndex+3] = x
		if parentID == 'root':
			childID = []
		else:
			childID = list(parentID)
		childID.append('down')
		nbr.List.append(child)
		nbr.ID.append(childID)


	if zIndex%3 != 0: # 'left'
		child = list(parent)
		y = parent[zIndex-1]
		child[zIndex]=y
		child[zIndex-1]=x
		if parentID == 'root':
			childID = []
		else:
			childID = list(parentID)
		childID.append('left')
		nbr.List.append(child)
		nbr.ID.append(childID)


	if zIndex%3 != 2: # 'right'
		child = list(parent)
		y = parent[zIndex+1]
		child[zIndex]=y
		child[zIndex+1]=x
		if parentID == 'root':
			childID = []
		else:
			childID = list(parentID)
		childID.append('right')
		nbr.List.append(child)
		nbr.ID.append(childID)


	return nbr






class state(list):

    def __init__(self, parentState,parentID):
    	self.parentState = parentState
    	self.nbr = makeNeighbours(parentState,parentID)


def BFS(initialState):

	frontier = Queue(maxsize=0)
	IDList = Queue(maxsize=0)
	x = state(initialState,'root')
	frontier.put(initialState)
	IDList.put('root')
	explored=[]
	exploredID = []

	""" stuff i need to output """
	path_to_goal = []
	nodes_expanded = []
	fringe_size = []
	frontier_size_list = []
	max_fringe_size = []
	search_depth = []
	max_search_depth = []
	depth_list = []




	while not frontier.empty():
		frontier_size = frontier.qsize()
		frontier_size_list.append(frontier_size)
		currentList =  frontier.get()
		frontier.task_done()
		currentID = IDList.get()
		IDList.task_done()
#		print currentList,currentID
		currentState = state(currentList,currentID)
		nodes_expanded = len(explored)
		explored.append(currentList)
		exploredID.append(currentID)
#		print exploredID


		if currentList == [0,1,2,3,4,5,6,7,8]:
			path_to_goal = list(currentID)
			fringe_size = frontier.qsize()
			max_fringe_size = max(frontier_size_list)
			cost_of_path = len(path_to_goal)
			search_depth = len(path_to_goal)
			for i in exploredID:
				element_depth = len(i)
				depth_list.append(element_depth)
			max_search_depth = max(depth_list)


			print "path_to_goal:", path_to_goal
			print "nodes_expanded:", nodes_expanded
			print "fringe_size:", fringe_size
			print "max_fringe_size:", max_fringe_size
			print "cost_of_path:", cost_of_path
			print "search_depth:", search_depth
			print "max search_depth:", max_search_depth
			print 'time in seconds:', time.clock() - start_time
#			print "maximum ram usage", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000   # should run only in LINUX
		else:
			if currentState.nbr.List:  # true if currentState.nbr.List is not empty
				for neighbour in currentState.nbr.List:
					if neighbour not in frontier.queue:
						if neighbour not in explored:  # nested if statements used because 'or'ing them together was not working as expected
							neighbourIndex = currentState.nbr.List.index(neighbour) # since each element of ID and list share the index
							frontier.put(neighbour)
							IDList.put(currentState.nbr.ID[neighbourIndex])


	




x = BFS([1,2,5,3,4,0,6,7,8])



