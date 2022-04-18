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
    
    def getEnd(self):
        end = []
        for i in range (self.getNum()):
            if self.getAdj(i + 1) == 1:
                end.append(i + 1)
        return end

    def BFS(self, nd):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend
        
        '''counted = np.zeros(100,dtype = bool)'''
        return None

    def BFS_2(self, nd_from, nd_to):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path
        self.pred = []
        self.dis = []
        for i in range (100):
            self.dis.append(int(200))
        for i in range (100):
            self.pred.append(int(0))
        self.que = []
        self.route = []
        self.que.append(int(nd_to))
        self.dis[nd_to] = 0
        while True:
            for succ in self.nd_dict[self.que[0]].getSuccessors():
                if (self.dis[self.que[0]] + self.nd_dict[self.que[0]].getDis(int(succ[0]))) < self.dis[int(succ[0])] :
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
        if len(self.turn) >= 3:
            self.action.append('F')
            for i in range (len(self.turn)-2):
                dir_start = 0
                dir_end = 0
                for succ in self.nd_dict[self.turn[i+1]].getSuccessors():
                    if succ[0] == self.turn[i]:
                        dir_start = succ[1]
                    elif succ[0] == self.turn [i+2]:
                        dir_end = succ[1]

                if (dir_end - dir_start + 4) % 4 == 2: ##直走
                    self.action.append('F')
                elif (dir_end - dir_start + 4) % 4 == 3: ##右轉
                    self.action.append('R')
                elif (dir_end - dir_start + 4) % 4 == 1: ##左轉
                    self.action.append('L')
                elif (dir_end - dir_start + 4) % 4 == 0: ##迴轉
                    self.action.append('B')
            self.action.append('B')
            self.action.pop(0) 
        return self.action
    
    def getTotalAction(self):
        end = self.getEnd()
        acroute = []
        start = self.getStartPoint()
        for i in range (len(end) - 1):
            for j in range(len(self.getAction(end[i], end[i + 1]))):
                acroute.append(self.getAction(end[i], end[i + 1])[j])
        acroute.append('S')
        end.pop(0)
        while True:
            j = -1
            for i in range (len(end)-2, -1, -1):
                if end[i] < end[i + 1]:
                    j = i
                    break
            
            if j == -1:
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
            route = []
            for i in range (len(self.getAction(1,end[0]))):
                route.append(self.getAction(1,end[0])[i])
            for i in range (len(end) - 1):
                for l in range (len(self.getAction(end[i], end[i + 1]))):
                    route.append(self.getAction(end[i], end[i + 1])[l])
            route.append('S')
            print(route)
            if len(acroute) > len(route):
                acroute = route




    def strategy(self, nd):
        return self.BFS(nd)

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)

if __name__ == '__main__':
    mz = Maze("medium_maze.csv")
    mz.getTotalAction()