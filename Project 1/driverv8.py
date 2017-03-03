# PLEASE NOTE: LEARN ABOUT HOW TO USE DICTIONARIES AND HOW TO SAVE MEMORY SPACE
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
		self.action = []  # stores the action from parent to child node

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

def makeNeighboursDFS(parent):
	zIndex = parent.index(0)

	x = parent[zIndex]
	
	nbr = neighboursDFS()

	if zIndex%3 != 2: # 'right'
		child = parent[:]
		y = parent[zIndex+1]
		child[zIndex]=y
		child[zIndex+1]=x
		nbr.List.append(child)
		nbr.action.append('Right')

	if zIndex%3 != 0: # 'left'
		child = parent[:]
		y = parent[zIndex-1]
		child[zIndex]=y
		child[zIndex-1]=x
		nbr.List.append(child)
		nbr.action.append('Left')


	if zIndex <6: # list for down
		child = parent[:]
		y = parent[zIndex+3]
		child[zIndex] = y
		child[zIndex+3] = x
		nbr.List.append(child)
		nbr.action.append('Down')

	if zIndex > 2: # list for 'up'
		child = parent[:] # use this to clone a list, not child = parent (which changes parent every time child changes)
		y = parent[zIndex-3]
		child[zIndex] = y
		child[zIndex-3] = x
		nbr.List.append(child)
		nbr.action.append('Up')

	return nbr






class stateBFS(list):

    def __init__(self, parentState,parentID):
    	self.parentState = parentState
    	self.nbr = makeNeighboursBFS(parentState,parentID)

class stateDFS(list):

    def __init__(self, parentState):
#    	self.parentState = parentState
    	self.nbr = makeNeighboursDFS(parentState)


def BFS(initialState):

	frontier = Queue(maxsize=0)
	IDList = Queue(maxsize=0)
#	x = stateBFS(initialState,'root')
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
			json.dump(path_to_goal,f)
			f.write('\n')
			f.write('cost_of_path: '+str(cost_of_path)+'\n')
			f.write('nodes_expanded: '+str(nodes_expanded)+'\n')
			f.write('fringe_size: '+str(fringe_size)+'\n')
			f.write('max_fringe_size: '+str(max_fringe_size)+'\n')
			f.write('cost_of_path: '+str(cost_of_path)+'\n')
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


	
def DFS(initialState):
	frontier= []
	frontierSet = set()
	initialStateStr = str(initialState)
	frontierSet.add(initialStateStr)
	ParentDict ={} 	# Dictionary to store parent state
	ActionDict = {}	# Dictionary to store action taken to get to child from parent
	ParentDict[initialStateStr] = 0 # Intiial state has parent 0
	ActionDict[initialStateStr] = 0 # Initial state has action 0
#	IDList = []
#	x=stateDFS(initialState,'root')
	frontier.append(initialState)
#	IDList.append('root')
	explored = set()
#	exploredID = []

	""" stuff i need to output """
	# path_to_goal = []
	# nodes_expanded = []
	# fringe_size = []
	# frontier_size_list = []
	# max_fringe_size = []
	# search_depth = []
	# max_search_depth = []
	# depth_list = []

	while len(frontier)>0: # until frontier is empty

		currentList = frontier.pop()
		currentListStr = str(currentList)
		frontierSet.remove(currentListStr)
#		currentID = IDList.pop()
		currentState = stateDFS(currentList)
		currentStr=str(currentList)
		explored.add(currentStr)
#		exploredID.append(currentID)
#		print "current ID: ", currentID
#		print "frontier ID: ", IDList
#		print currentState.nbr.ID
#		os.system("pause")
#		print explored
		if currentList == [0,1,2,3,4,5,6,7,8]:
			getpath =[]
			while ParentDict[currentListStr] !=0:
				getpath.append(ActionDict[currentListStr])
				currentListStr=ParentDict[currentListStr]
			getpath.reverse()			
			print getpath
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
#							IDList.append(currentState.nbr.ID[neighbourIndex])




x = DFS([1,2,5,3,4,0,6,7,8])



