from Queue import Queue
import time
import json
import os
from copy import copy
from heapq import *  # since we are using heaps
import itertools  # used for the count
start_time = time.clock()

""" returns the co-ordinate of any number in the 3*3 puzzle """
def getManhattanCoord(puzzle,i):

	noIndex = puzzle.index(i)

	x = noIndex/3
	y = noIndex%3

	return x,y

""" generates the (should be) co-ordinate of any number in the puzzle,i.e., 1 should have co-ord:(0,1), 2:(0,2),3:(1,0) and so on... """
def generateManhattanCoord(i):

	if i in range(1,9):
		x = i/3
		y=i%3
		return x,y
	else:
		print "Error: Number has no place in the puzzle"

""" calculates the total Manhattan Distance of all the numbers in the 3*3 puzzle (except for 0) 
Manhattan Distance Calculation technique: http://math.stackexchange.com/questions/139600/how-to-calculate-the-euclidean-and-manhattan-distance
Video: https://courses.edx.org/courses/course-v1:ColumbiaX+CSMM.101x+1T2017/courseware/de0319e8ff964eb5bc9163a610387086/8124a8a8b4c64c718d85f4990aa5d4ed/
"""
def ManhattanDistanceCalculator(puzzle):

	ManhattanDistance=0
	for i in puzzle:
		if i!=0:
			[a,b] = generateManhattanCoord(i)
			[c,d] = getManhattanCoord(puzzle,i)

			ManhattanDistance+=abs(a-c)+abs(b-d)

	return ManhattanDistance



""" creates neighbour class used for Astar search """
class neighboursAstar(object):

	def __init__(self):
		self.List = []  # Stores a list of neighbours of the current state
		self.action = []  # stores the action(direction) from parent to child node
		self.depth = []	# stores the depth of the corresponding node
		self.cost = [] # stores the cost function value (depth + Manhattan distance to goal)


def makeNeighboursAstar(parent,parentDepth): # The depth is the cost to get from root to current node
	zIndex = parent.index(0)

	x = parent[zIndex]
	
	nbr = neighboursAstar()
	neighbourDepth = parentDepth+1



	if zIndex%3 != 2: # 'right'
		child = parent[:] # use this to clone a list, not child = parent (which changes parent every time child changes)
		y = parent[zIndex+1]
		child[zIndex]=y
		child[zIndex+1]=x
		goalCost = neighbourDepth + ManhattanDistanceCalculator(child)
		nbr.List.append(child)
		nbr.action.append('Right')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(goalCost)
		

	if zIndex%3 != 0: # 'left'
		child = parent[:]
		y = parent[zIndex-1]
		child[zIndex]=y
		child[zIndex-1]=x
		goalCost = neighbourDepth + ManhattanDistanceCalculator(child)
		nbr.List.append(child)
		nbr.action.append('Left')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(goalCost)


	if zIndex <6: # 'down'
		child = parent[:]
		y = parent[zIndex+3]
		child[zIndex] = y
		child[zIndex+3] = x
		goalCost = neighbourDepth + ManhattanDistanceCalculator(child)
		nbr.List.append(child)
		nbr.action.append('Down')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(goalCost)

	if zIndex > 2: # 'up'
		child = parent[:] 
		y = parent[zIndex-3]
		child[zIndex] = y
		child[zIndex-3] = x
		goalCost = neighbourDepth + ManhattanDistanceCalculator(child)
		nbr.List.append(child)
		nbr.action.append('Up')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(goalCost)
		
	return nbr

class stateAstar(list):

    def __init__(self, currentList,currentDepth):
    	self.nbr = makeNeighboursAstar(currentList,currentDepth)

entry_finder = {}               # dictionary pointing to an entry in the frontier
counter = itertools.count()     # unique sequence count


def add_state(frontier,state, cost,stateStr,depth):
    """Add a new state to the frontier heap"""

    count = next(counter)
    entry = [cost, count, state,stateStr,depth]
    entry_finder[stateStr] = entry
    heappush(frontier, entry)


def update_state(frontier,cost,stateStr,depth):
	""" used to update the cost of the state """
	previousEntry = entry_finder[stateStr]
	getEntryIndex = frontier.index(previousEntry)
	previousCost = frontier[getEntryIndex][0] # get previously stored cost of the state

	""" if cost < previousCost, then replace the previous cost with the new one in frontier for the state """
	if cost<previousCost:
		newEntry = previousEntry[:] 
		newEntry[0]=cost
		newEntry[-1]=depth
		entry_finder[stateStr]=newEntry
		frontier[getEntryIndex]=newEntry





def update_parent(frontier,neighbourStateStr,neighbourCost, currentStateStr,currentState,neighbourIndex,ParentDict,ActionDict):
	""" uodates the parent and action dictionaries if the new cost of neighbour in frontier less than previous one"""
	previousCost = entry_finder[neighbourStateStr][0]
	if neighbourCost<previousCost:
		ParentDict[neighbourStateStr]=currentStateStr
		ActionDict[neighbourStateStr]=currentState.nbr.action[neighbourIndex]



""" main function for Astar """
def Astar(initialState):
	frontier = [] # frontier is a heap (a list which is sorted in ascending order)
	frontierSet = set()
	initialStateStr = str(initialState)
	frontierSet.add(initialStateStr)
	ParentDict = {} # Dictionary to store parent state
	ActionDict = {} # Dictionary to store the action taken to get to child from parent
	ParentDict[initialStateStr] = 0
	ActionDict[initialStateStr]=0
	initialDepth = 0
	explored = set()

	initialCost = 0 + ManhattanDistanceCalculator(initialState)
	add_state(frontier,initialState,initialCost,initialStateStr,initialDepth)
	""" variables needed to be output at the end"""
	# nodes_expanded = 0
	max_fringe_size = 0
	# search_depth = 0
	max_search_depth = 0




	while len(frontier)>0:
		currentStateInfo = heappop(frontier) 

		if len(frontier)>max_fringe_size:
			max_fringe_size=len(frontier)

		currentStateCost=currentStateInfo[0]
		currentStateCount=currentStateInfo[1]
		currentStateList = currentStateInfo[2] # currentStateInfo[1] is the count of the state
		currentStateStr = currentStateInfo[3]
		currentStateDepth = currentStateInfo[4]

		if max_search_depth<currentStateDepth:
			max_search_depth=currentStateDepth

		frontierSet.remove(currentStateStr) # used for searching for states in the else loop below
		nodes_expanded=len(explored)
		explored.add(currentStateStr)


		currentState = stateAstar(currentStateList,currentStateDepth) # This class actually stores all the neighbour info of the currentState

		if currentStateList == [0,1,2,3,4,5,6,7,8]:
			getpath=[]

			while currentStateStr!=initialStateStr:
				getpath.append(ActionDict[currentStateStr])
				currentStateStr=ParentDict[currentStateStr]

			getpath.reverse()
#			print getpath
			fringe_size = len(frontier)
			cost_of_path=len(getpath)
			search_depth = cost_of_path
			time_in_seconds = time.clock() - start_time

			tf = 'output.txt'
			f=open(tf,'w')
			line1 = 'path_to_goal: '
			f.write('line1')
			json.dump(getpath,f)
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
					if neighbourStr not in explored:
						if neighbourStr not in frontierSet:
							neighbourIndex=currentState.nbr.List.index(neighbour)
							ParentDict[neighbourStr]=currentStateStr
							ActionDict[neighbourStr]=currentState.nbr.action[neighbourIndex]
							neighbourCost=currentState.nbr.cost[neighbourIndex]
							neighbourDepth = currentState.nbr.depth[neighbourIndex]
							add_state(frontier,neighbour,neighbourCost,neighbourStr,neighbourDepth)
							frontierSet.add(neighbourStr)

						else: # if neighbour is in frontierSet and this time it has shorter cost, then we need to update the neighbour's cost function, parent node, action from parent node and depth
							neighbourIndex=currentState.nbr.List.index(neighbour)
							neighbourCost=currentState.nbr.cost[neighbourIndex]
							update_parent(frontier,neighbourStr,neighbourCost, currentStateStr,currentState,neighbourIndex,ParentDict,ActionDict)
							update_state(frontier,neighbourCost,neighbourStr,neighbourDepth)


x=Astar([4,7,8,1,6,3,5,0,2])


						 












