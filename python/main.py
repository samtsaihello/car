from node import *
import maze as mz
import score
import interface
import time

import numpy as np
import pandas
import time
import sys
import os

def main():
    maze = mz.Maze("small_maze.csv")
    #point = score.Scoreboard("UID.csv", "team_NTUEE", " http://140.112.175.15:3000")
    #interf = interface.interface()
    # TODO : Initialize necessary variables
    start = maze.getStartPoint()

    #if (sys.argv[1] == '0'):
    print("Mode 0: for treasure-hunting")
    # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
    end = maze.getEnd()
    for nd in end:
        if (not maze.getCounted(nd)) and nd != start: 
            print(maze.getAction(start, nd))
            start = nd
    
        
    #elif (sys.argv[1] == '1'):
        #print("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.

if __name__ == '__main__':
    main()
