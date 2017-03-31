""" Calculate no. of misplaced tiles in a 3*3 puzzle (8 puzzle) """
def calcMisplacedTiles(puzzle):

	count = 0


	for i in range(1,len(puzzle)):

		if puzzle[i]!=i:
			count +=1

	return count

""" Test the function """
x = calcMisplacedTiles([0,1,2,3,5,4,6,7,8])
print x





