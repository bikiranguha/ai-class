from heapq import *

unordered_list=[0,5,4,2,6,3,7,8]

ordered_list=[]
temp=[] # buffer to store the sorted values
for value in unordered_list:
    heappush(temp,value)


for i in range(len(temp)):
    ordered_list.append(heappop(temp)) # heappop pops the smallest element first

print ordered_list
    
