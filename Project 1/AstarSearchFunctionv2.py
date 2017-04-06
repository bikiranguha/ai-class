from Queue import Queue
from Queue import PriorityQueue
import time
import json
import os
from copy import copy
from heapq import *  # since we are using heaps
import itertools  # used for thec count

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
		child = parent[:]
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


	if zIndex <6: # list for down
		child = parent[:]
		y = parent[zIndex+3]
		child[zIndex] = y
		child[zIndex+3] = x
		goalCost = neighbourDepth + ManhattanDistanceCalculator(child)
		nbr.List.append(child)
		nbr.action.append('Down')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(goalCost)

	if zIndex > 2: # list for 'up'
		child = parent[:] # use this to clone a list, not child = parent (which changes parent every time child changes)
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
REMOVED = '<removed-task>'      # placeholder for a removed task
counter = itertools.count()     # unique sequence count


def add_state(frontier,state, cost,stateStr,depth):
    """Add a new state"""
    # if stateStr in entry_finder:
    # 	previousCost = entry_finder[stateStr][0]
    # 	if cost < previousCost:
    # 		remove_state(stateStr)
    count = next(counter)
    entry = [cost, count, state,stateStr,depth]
    entry_finder[stateStr] = entry
    heappush(frontier, entry)

#def update_state(frontier,state,cost,count,stateStr,depth):
def update_state(frontier,cost,stateStr,depth):
	""" used to update the cost of states """
	previousEntry = entry_finder[stateStr]
	getEntryIndex = frontier.index(previousEntry)
	previousCost = frontier[getEntryIndex][0]
	if cost<previousCost:
		newEntry = previousEntry[:]
		newEntry[0]=cost
		newEntry[-1]=depth
		entry_finder[stateStr]=newEntry
		frontier[getEntryIndex]=newEntry
#		remove_state(stateStr)
#		count = next(counter)
#		entry = [cost, count, state,stateStr,depth]
#		entry_finder[stateStr] = entry
#		heappush(frontier, entry)


# def remove_state(stateStr):
#     """Mark an existing state as REMOVED.  """
#     entry = entry_finder.pop(stateStr)
#     entry[-1] = REMOVED

def update_parent(frontier,neighbourStateStr,neighbourCost, currentStateStr,currentState,neighbourIndex,ParentDict,ActionDict):
	""" uodates the parent and action dictionaries if the new cost of neighbour in frontier less than previous one"""
	previousCost = entry_finder[neighbourStateStr][0]
	if neighbourCost<previousCost:
		ParentDict[neighbourStateStr]=currentStateStr
		ActionDict[neighbourStateStr]=currentState.nbr.action[neighbourIndex]




def Astar(initialState):
	frontier = [] # frontier is a heap which is actually a list which is sorted
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
#	print frontier


	while len(frontier)>0:
		currentStateInfo = heappop(frontier) # Should be able to handle ties in cost with the count parameter, which is unique for every state
#		print currentStateInfo
		currentStateCost=currentStateInfo[0]
		currentStateCount=currentStateInfo[1]
		currentStateList = currentStateInfo[2] # currentStateInfo[1] is the count of the state
		currentStateStr = currentStateInfo[3]
		currentStateDepth = currentStateInfo[4]
#		print explored
		frontierSet.remove(currentStateStr) # used for searching for states in the else loop below
		explored.add(currentStateStr)


		currentState = stateAstar(currentStateList,currentStateDepth) # This class actually stores all the neighbour info of the currentState, consider renaming this later

		if currentStateList == [0,1,2,3,4,5,6,7,8]:
			getpath=[]

			while currentStateStr!=initialStateStr:
				getpath.append(ActionDict[currentStateStr])
				currentStateStr=ParentDict[currentStateStr]

			getpath.reverse()
			print getpath

#			print 'Yay, found the goal!'
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
#							update_state(frontier,neighbour,neighbourCost,currentStateCount,neighbourStr,neighbourDepth)
							update_state(frontier,neighbourCost,neighbourStr,neighbourDepth)


x=Astar([1,2,5,3,4,0,6,7,8])


						 












