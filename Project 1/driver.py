from Queue import Queue
import time
import json
import os
from copy import copy
#import resource # uncomment when running in linux
start_time = time.clock()


class neighboursDFS(object):

	def __init__(self):
		self.List = []  # Stores a list of neighbours of the current state
		self.action = []  # stores the action(direction) from parent to child node
		self.depth = []	# stores the depth of the corresponding node

class neighbours(object):

	def __init__(self):
		self.List = []  # Stores a list of neighbours of the current state
		self.ID = []  # ID stores the direction from the root node of the current state

def makeNeighboursBFS(parent,parentID):
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

def makeNeighboursDFS(parent,parentDepth):
	zIndex = parent.index(0)

	x = parent[zIndex]
	
	nbr = neighboursDFS()
#	nbr.depth = depth+1

	if zIndex%3 != 2: # 'right'
		child = parent[:]
		y = parent[zIndex+1]
		child[zIndex]=y
		child[zIndex+1]=x
		nbr.List.append(child)
		nbr.action.append('Right')
		nbr.depth.append(parentDepth+1)
		

	if zIndex%3 != 0: # 'left'
		child = parent[:]
		y = parent[zIndex-1]
		child[zIndex]=y
		child[zIndex-1]=x
		nbr.List.append(child)
		nbr.action.append('Left')
		nbr.depth.append(parentDepth+1)


	if zIndex <6: # list for down
		child = parent[:]
		y = parent[zIndex+3]
		child[zIndex] = y
		child[zIndex+3] = x
		nbr.List.append(child)
		nbr.action.append('Down')
		nbr.depth.append(parentDepth+1)

	if zIndex > 2: # list for 'up'
		child = parent[:] # use this to clone a list, not child = parent (which changes parent every time child changes)
		y = parent[zIndex-3]
		child[zIndex] = y
		child[zIndex-3] = x
		nbr.List.append(child)
		nbr.action.append('Up')
		nbr.depth.append(parentDepth+1)
		

	return nbr






class stateBFS(list):

    def __init__(self, parentState,parentID):
    	self.parentState = parentState
    	self.nbr = makeNeighboursBFS(parentState,parentID)

class stateDFS(list):

    def __init__(self, currentList,currentDepth):
    	self.nbr = makeNeighboursDFS(currentList,currentDepth)


def BFS(initialState):

	frontier = Queue(maxsize=0)
	IDList = Queue(maxsize=0)
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
		currentState = stateBFS(currentList,currentID)
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
			time_in_seconds = time.clock() - start_time
#			max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000; # uncomment in ubuntu
			tf = 'output.txt'
			f = open(tf,'w')
			line1 = 'path_to_goal: '
			f.write(line1)
			json.dump(path_to_goal,f) # used to write the list 'path_to_goal'
			f.write('\n')
			f.write('cost_of_path: '+str(cost_of_path)+'\n')
			f.write('nodes_expanded: '+str(nodes_expanded)+'\n')
			f.write('fringe_size: '+str(fringe_size)+'\n')
			f.write('max_fringe_size: '+str(max_fringe_size)+'\n')
			f.write('search_depth: '+str(search_depth)+'\n')
			f.write('max_search_depth: '+str(max_search_depth)+'\n')
			f.write('time_in_seconds: '+str(time_in_seconds)+'\n')
#			f.write('max_ram_usage: '+str(max_ram_usage)+'\n') # uncomment in ubuntu
			f.close()


		else:
			if currentState.nbr.List:  # true if currentState.nbr.List is not empty
				for neighbour in currentState.nbr.List:
					if neighbour not in frontier.queue:
						if neighbour not in explored:  # nested if statements used because 'or'ing them together was not working as expected
							neighbourIndex = currentState.nbr.List.index(neighbour) # since each element of ID and list share the index
							frontier.put(neighbour)
							IDList.put(currentState.nbr.ID[neighbourIndex])


	
def DFS(initialState): # Note that the search path will vary depend on the order of visits of the node
	frontier= []
	frontierSet = set() # searching in sets is much faster than lists
	initialStateStr = str(initialState)
	frontierSet.add(initialStateStr)
	ParentDict ={} 	# Dictionary to store parent state
	ActionDict = {}	# Dictionary to store action taken to get to child from parent
	ParentDict[initialStateStr] = 0 # Intiial state has parent 0
	ActionDict[initialStateStr] = 0 # Initial state has action 0
	nodes_expanded = 0
	max_fringe_size = 0
	search_depth=0
	max_search_depth = 0
	depthList = [0] # stores the depth of the corresponding elements in frontier


	frontier.append(initialState)
	explored = set()



	while len(frontier)>0: # until frontier is empty
		if len(frontier)>max_fringe_size:
			max_fringe_size = len(frontier)
		currentList = frontier.pop()
		currentListStr = str(currentList)
		frontierSet.remove(currentListStr)
		currentDepth = depthList.pop()
		currentState = stateDFS(currentList,currentDepth)
		if max_search_depth<currentDepth:
			max_search_depth =currentDepth
		currentStr=str(currentList)
		nodes_expanded=len(explored)
		explored.add(currentStr)
#		os.system("pause")
		if currentList == [0,1,2,3,4,5,6,7,8]:
			getpath =[]

			while currentListStr != initialStateStr:  
				getpath.append(ActionDict[currentListStr])
				currentListStr=ParentDict[currentListStr]
			getpath.reverse()
			fringe_size=len(frontier)
			# print"path_to_goal: ",getpath
			cost_of_path=len(getpath)
			time_in_seconds = time.clock() - start_time
			search_depth=len(getpath)
			# print "cost_of_path: ",cost_of_path
			# print "nodes expanded: ",nodes_expanded
			# print "fringe size: ", len(frontier)
			# print "max_fringe_size: ", max_fringe_size
			# print "search_depth: ", len(getpath)
			# print "max_search_depth", max_search_depth
			tf = 'output.txt'
			f=open(tf,'w')
			line1 = 'path_to_goal: '
			f.write(line1)
			json.dump(getpath,f) # used to write the list 'path_to_goal'. f.write cannot write lists directly to text file
			f.write('\n')
			f.write('cost_of_path: '+str(cost_of_path)+'\n')
			f.write('nodes_expanded: '+str(nodes_expanded)+'\n')
			f.write('fringe_size: '+str(fringe_size)+'\n')
			f.write('max_fringe_size: '+str(max_fringe_size)+'\n')
			f.write('search_depth: '+str(search_depth)+'\n')
			f.write('max_search_depth: '+str(max_search_depth)+'\n')
			f.write('time_in_seconds: '+str(time_in_seconds)+'\n')
#			f.write('max_ram_usage: '+str(max_ram_usage)+'\n') # uncomment in ubuntu
			f.close()


			break


		else:
			if currentState.nbr.List:
				for neighbour in currentState.nbr.List:
					neighbourStr = str(neighbour)
					if neighbourStr not in frontierSet:
						if neighbourStr not in explored:
							neighbourIndex = currentState.nbr.List.index(neighbour)
							ParentDict[neighbourStr] = currentListStr
							ActionDict[neighbourStr] = currentState.nbr.action[neighbourIndex]
							frontier.append(neighbour)
							frontierSet.add(neighbourStr)
							depthList.append(currentState.nbr.depth[neighbourIndex])





x = DFS([1,2,5,3,4,0,6,7,8])
#x = DFS([3,1,2,6,4,5,7,8,0])



