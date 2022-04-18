
from collections import *

column,row = 4,100
adj = [[0] * column for _ in range(row)]
pred = [0] * 100
dis = [0] * 100
num_of_adj = [0] * 100
import numpy as np
counted = np.zeros(100,dtype = bool)
cannotfind = False

num = int (input())
start = int (input())
end = int (input())
for i in range(1,num+1):
    num_of_adj[i] = int(input())
    if num_of_adj[i] == 0:
        continue
    else:
        for j in range(0,num_of_adj[i]):
            adj[i][j] = int(input())

deq = deque()
deq.appendleft(end) #add element on the left side
dis[end] = 0
start_appear = False
while True:
    for i in range (0,num_of_adj[deq[0]]):
        if counted[(adj[deq[0]][i])]==0:
            counted[(adj[deq[0]][i])] = 1
            deq.append(adj[deq[0]][i]) #add element on the right side
            dis[adj[deq[0]][i]] = dis[deq[0]] + 1
            if pred[adj[deq[0]][i]] == 0:
                pred[adj[deq[0]][i]] = deq[0]
            if adj[deq[0]][i] == start:
                start_appear = True
                break
    if start_appear == True:
        break
    if len(deq) == 1:
        cannotfind = True
        break
    else:
        deq.popleft()  #eliminate the first element
        
present = start
if cannotfind == 'True':
    print("We can't find a path!")
else:
    for i in range(dis[start]+1,1,-1):
        print(pred[present],"",) #two quotation marks and a comma represents " "
        present = pred[present]
    
