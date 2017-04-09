import sys

# sys.argv[0] is the name of the script. The latter arguments: sys.argv[1], sys.argv[2] and so on are the arguments passed
x = float(sys.argv[1]) # sys.argv elements are strings, so need to convert the first argument to float to do the multiplications
lst = sys.argv[2]
print "Double the number passed:", 2*x
print "Square of the number passed:", x*x
print "List: ", lst
