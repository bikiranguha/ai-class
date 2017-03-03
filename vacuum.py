

def vacuumagent(location,state):
	""" Vacuum cleaning algorithm: Gets the location (A or B) and state (clean or dirty).
	If A is dirty, then 'suck', else go right
	If B is dirty, then 'suck', else go left.
"""
	if state=='dirty':
		return 'suck'
	elif location == 'A':
		return 'right'
	elif location == 'B':
		return 'left'