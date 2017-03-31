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

dist = ManhattanDistanceCalculator([1,5,3,8,7,4,2,0,6])
print dist

