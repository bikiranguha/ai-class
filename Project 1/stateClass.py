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

# l = [0,1,2,3,4,5,6,7,8]
# cU = move(l,'up')
# cD = move(l,'down')
# cR = move(l,'right')
# cL = move(l,'left')
# print l
# print cU
# print cD
# print cL
# print cR





class state(list):

    def __init__(self, parentState):
    	self.parentState = parentState
#    	self.emptyIndex = parentState.index(0)

    	self.childUp = move(self.parentState,'up')
    	self.childDown = move(self.parentState,'down')
    	self.childLeft = move(self.parentState,'left')
    	self.childRight = move(self.parentState,'right')
    	self.neighbours = [self.childUp,self.childDown,self.childRight,self.childLeft]





x = state([1,2,4,3,5,0,6,8,7])
print x.parentState
print x.childUp
print x.childDown
print x.childLeft
print x.childRight
print x.neighbours
