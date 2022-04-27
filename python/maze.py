from node import *
import numpy as np
import csv
import pandas
from enum import IntEnum
import math
import collections

class Action(IntEnum):
    FRONT = 1
    RETURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath):
        # TODO : read file and implement a data structure you like
		# For example, when parsing raw_data, you may create several Node objects.  
		# Then you can store these objects into self.nodes.  
		# Finally, add to nd_dictionary by {key(index): value(corresponding node)}
        self.raw_data = pandas.read_csv(filepath)
        self.num = len(self.raw_data.index)
        self.adj_num = []
        self.counted = []
        for i in range (100):
            self.counted.append(0)
        self.nodes = []
        self.nd_dict = dict()  # key: index, value: the correspond node
        self.bfsdis = [[0 for _ in range(self.num + 1)] for _ in range(self.num + 1)]
        
        for i in range (self.num):
            d = Node (i+1)
            coun = 0
            if not np.isnan(self.raw_data['North'][i]):
                d.setSuccessor(self.raw_data['North'][i],3,self.raw_data['ND'][i])
                coun += 1
            if not np.isnan(self.raw_data['South'][i]):
                d.setSuccessor(self.raw_data['South'][i],1,self.raw_data['SD'][i])
                coun += 1
            if not np.isnan(self.raw_data['West'][i]):
                d.setSuccessor(self.raw_data['West'][i],2,self.raw_data['WD'][i])
                coun += 1
            if not np.isnan(self.raw_data['East'][i]):
                d.setSuccessor(self.raw_data['East'][i],4,self.raw_data['ED'][i])
                coun += 1
            
            self.nd_dict[i+1] = d
            self.adj_num.append(coun)

    def getNum(self):
        return self.num

    def getAdj(self, nd):
        return self.adj_num[nd - 1]

    def getStartPoint(self):
        if (len(self.nd_dict) < 2):
            print("Error: the start point is not included.")
            return 0
        return self.nd_dict[1].index
    def getNodeDict(self):
        return self.nd_dict

    def getCounted(self, nd):
        return self.counted[nd]
    
    def getMDistance(self, nd_from, nd_to):
        route = self.BFS_2(nd_from, nd_to)
        x = 0
        y = 0
        r = 0
        for i in range (len(route) - 1):
            dir = self.getNodeDict()[route[i]].getDirection(route[i + 1])
            dis = self.getNodeDict()[route[i]].getDis(route[i + 1])
            if dir == 3: x += dis
            elif dir == 1: x -= dis
            elif dir == 4: y += dis
            else: y -= dis
        if x < 0: x = -x
        if y < 0: y = -y
        r = x + y
        return r
    
    def getEnd(self):
        end = []
        for i in range (self.getNum()):
            if self.getAdj(i + 1) == 1:
                end.append(i + 1)
        if end[0] == 1:
            end.pop(0) #1不包含於 end point
        return end

    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        
        '''counted = np.zeros(100,dtype = bool)'''
        return None

    def TurnDirection(self, dir_end, dir_start):
        if (dir_end - dir_start + 4) % 4 == 2: ##直走
            return 'F'
        elif (dir_end - dir_start + 4) % 4 == 3: ##右轉
            return 'R'
        elif (dir_end - dir_start + 4) % 4 == 1: ##左轉
            return 'L'
        elif (dir_end - dir_start + 4) % 4 == 0: ##迴轉
            return 'B'


    def BFS_2(self, nd_from, nd_to):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        self.pred = []
        self.dis = []
        straight = 4
        turn_time = 6
        back = 7
        for i in range (100):
            self.dis.append(int(1000))
        for i in range (100):
            self.pred.append(int(0))
        self.que = []
        self.route = []
        self.que.append(int(nd_to))
        self.dis[nd_to] = 0
        while True:
            for succ in self.nd_dict[self.que[0]].getSuccessors():
                exp_dis = self.dis[self.que[0]] + self.nd_dict[self.que[0]].getDis(int(succ[0])) * straight
                dir_end = succ[1]
                dir_start = self.pred[self.que[0]]
                turn = self.TurnDirection(dir_end, dir_start)
                if turn == 'F': exp_dis += straight
                elif turn == 'R' or turn == 'L': exp_dis += turn_time
                elif turn == 'B': exp_dis += back
                if (exp_dis) < self.dis[int(succ[0])] :
                    self.que.append(int(succ[0]))
                    self.dis[int(succ[0])] = self.dis[self.que[0]] + self.nd_dict[self.que[0]].getDis(int(succ[0]))
                    self.pred[int(succ[0])] = self.que[0]
            if len(self.que) == 1:
                break
            else:
                self.que.pop(0)

        present = nd_from
        self.route.append(nd_from)
        while True:
            present = self.pred[present]
            self.route.append(present)
            if present == nd_to:
                break
        for a in self.route:
            self.counted[a] = 1 
        
        return self.route

    def getAction(self, nd_from, nd_to):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the nd_to is the Successor of nd_to
		# If not, print error message and return 0
        self.turn = self.BFS_2(nd_from, nd_to)
        self.action = []
        for i in range (len(self.turn)-2):
            dir_start = 0
            dir_end = 0
            for succ in self.nd_dict[self.turn[i+1]].getSuccessors():
                if succ[0] == self.turn[i]:
                    dir_start = succ[1]
                elif succ[0] == self.turn [i+2]:
                    dir_end = succ[1]
            self.action.append(self.TurnDirection(dir_end, dir_start))
        for en in self.getEnd():
            if nd_to == en:
                self.action.append('B')
        return self.action
    
    def getAllPathTime(self):
        for end in self.getEnd():
            time = 0
            index = self.BFS_2(1,end)
            act = self.getAction(1,end)
            for i in range(len(index) - 1):
                time += self.nd_dict[index[i]].getDis(index[i + 1])
            for a in act:
                if a == 'F': time += 1
                elif a == 'R' or a == 'L': time +=2
                elif a == 'B': time +=4
            self.bfsdis[1][end], self.bfsdis[end][1] = time, time
        _end = self.getEnd()
        for i in range(len(_end)):
            for j in range (i + 1, len(_end)):
                time = 0
                index = self.BFS_2(_end[i], _end[j])
                act = self.getAction(_end[i], _end[j])
                for l in range(len(index) - 1):
                    time += self.nd_dict[index[l]].getDis(index[l + 1])
                for a in act:
                    if a == 'F': time += 1
                    elif a == 'R' or a == 'L': time +=2
                    elif a == 'B': time +=4
                self.bfsdis[_end[i]][_end[j]], self.bfsdis[_end[j]][_end[i]] = time, time

    def getTotalAction(self):
        self.getAllPathTime()
        end = self.getEnd()
        start = self.getStartPoint()
        actime = self.bfsdis[start][end[0]]
        acroute = []
        for i in range (len(end) - 1):
            actime += self.bfsdis[end[i]][end[i + 1]]
        while True:
            j = -1
            for i in range (len(end)-2, -1, -1):
                if end[i] < end[i + 1]:
                    j = i
                    break
            
            if j == -1:
                print(actime)
                return acroute
            k = -1
            min = 200
            for i in range (j,len(end)):
                if end[i] > end[j] and end[i] <= min:
                    min = end[i]
                    k = i

            end[j], end[k] = end[k], end[j]
            left = j + 1
            right = len(end) - 1
            while left < right:
                end[left], end[right] = end[right], end[left]
                left += 1
                right -= 1
            time = self.bfsdis[start][end[0]]
            for i in range (len(end) - 1):
                time += self.bfsdis[end[i]][end[i + 1]]
            if time < actime:
                acroute = []
                for i in range(len(self.getAction(start, end[0]))):
                    acroute.append(self.getAction(start, end[0])[i])
                for i in range (len(end) - 1):
                    for l in range (len(self.getAction(end[i], end[i + 1]))):
                        acroute.append(self.getAction(end[i], end[i + 1])[l])
                acroute.append('S')
                actime = time

    def getTotalAction_2(self):
        self.getAllPathTime()
        end = self.getEnd()
        start = self.getStartPoint()
        acroute = []
        actime = 0
        acpath = []
        tem = []
        ldis = 0
        f_p = 0
        f_p_index = 0
        for i in range (len(end)):
            if self.getMDistance(start, end[i]) > ldis:
                ldis = self.getMDistance(start, end[i])
                f_p = end[i]
                i = f_p_index
        lroute = self.BFS_2(start, f_p)
        #check 兩個點以內是否有 end
        for i in lroute:
            for succ in self.nd_dict[i].getSuccessors():
                if not succ in lroute:
                    if (int(succ[0])) in end and (not int(succ[0]) in tem) and (int(succ[0]) != f_p):
                        tem.append(int(succ[0]))
                        for l in range(len(end)):
                            if end[l] == int(succ[0]):
                                end.pop(l)
                                break
                    else:
                        for succ_2 in self.nd_dict[int(succ[0])].getSuccessors():
                            if int(succ_2[0]) in end and (not int(succ_2[0]) in tem) and (int(succ_2[0]) != f_p):
                                tem.append(int(succ_2[0]))
                                for l in range(len(end)):
                                    if end[l] == int(succ_2[0]):
                                        end.pop(l)
                                        break
        tem.append(f_p)
        for i in range(len(end)):
            if end[i] == f_p: end.pop(i)
        acpath.append(start)
        while len(tem) != 0:
            acpath.append(tem[0])
            tem.pop(0)

        for i in range(len(acpath) - 1):
            actime += self.bfsdis[acpath[i]][acpath[i + 1]]
            for l in range(len(self.getAction(acpath[i], acpath[i + 1]))):
                acroute.append(self.getAction(acpath[i], acpath[i + 1])[l]) 
           
        if len(end) != 0:
            actime += self.bfsdis[acpath[-1]][end[0]]
            for i in range(len(self.getAction(acpath[-1], end[0]))):
                acroute.append(self.getAction(acpath[-1], end[0])[i]) 
            for i in range(1,len(end)):
                    actime += self.bfsdis[end[i - 1]][end[i]]
                    for l in range(len(self.getAction(end[i - 1], end[i]))):
                        acroute.append(self.getAction(end[i - 1], end[i])[l]) 
        acroute.append('S')
        #跑排列
        while True:
            j = -1
            for i in range (len(end)-2, -1, -1):
                if end[i] < end[i + 1]:
                    j = i
                    break
            
            if j == -1:
                print(actime)
                return acroute
            
            k = -1
            min = 200
            for i in range (j,len(end)):
                if end[i] > end[j] and end[i] <= min:
                    min = end[i]
                    k = i

            end[j], end[k] = end[k], end[j]
            left = j + 1
            right = len(end) - 1
            while left < right:
                end[left], end[right] = end[right], end[left]
                left += 1
                right -= 1
            time = 0
            for i in range(len(acpath) - 1):
                time += self.bfsdis[acpath[i]][acpath[i + 1]]
            if len(end) != 0:
                time += self.bfsdis[acpath[-1]][end[0]]
                for i in range(1,len(end)):
                    time += self.bfsdis[end[i - 1]][end[i]]
            if time < actime:
                acroute = []
                for i in range(len(acpath) - 1):
                    for l in range(len(self.getAction(acpath[i], acpath[i + 1]))):
                        acroute.append(self.getAction(acpath[i], acpath[i + 1])[l]) 
                if len(end) != 0:
                    for i in range(len(self.getAction(acpath[-1], end[0]))):
                        acroute.append(self.getAction(acpath[-1], end[0])[i]) 
                    for i in range(1,len(end)):
                        for l in range(len(self.getAction(end[i - 1], end[i]))):
                            acroute.append(self.getAction(end[i - 1], end[i])[l]) 
                acroute.append('S')
                actime = time
                
    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)

if __name__ == '__main__':
    mz = Maze("medium_maze.csv")
    print(mz.getTotalAction())
   