from Queue import Queue
import time
import json
import os
from copy import copy

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
		cost = neighbourDepth + ManhattanDistanceCalculator(child)
		nbr.List.append(child)
		nbr.action.append('Right')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(cost)
		

	if zIndex%3 != 0: # 'left'
		child = parent[:]
		y = parent[zIndex-1]
		child[zIndex]=y
		child[zIndex-1]=x
		nbr.List.append(child)
		nbr.action.append('Left')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(cost)


	if zIndex <6: # list for down
		child = parent[:]
		y = parent[zIndex+3]
		child[zIndex] = y
		child[zIndex+3] = x
		nbr.List.append(child)
		nbr.action.append('Down')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(cost)

	if zIndex > 2: # list for 'up'
		child = parent[:] # use this to clone a list, not child = parent (which changes parent every time child changes)
		y = parent[zIndex-3]
		child[zIndex] = y
		child[zIndex-3] = x
		nbr.List.append(child)
		nbr.action.append('Up')
		nbr.depth.append(neighbourDepth)
		nbr.cost.append(cost)
		

	return nbr