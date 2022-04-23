from turtle import width
from node import *
import maze as mz
import score
import interface
import time
import threading

import numpy as np
import pandas
import time
import sys
import os
def read():
    while True:
        msg = interf.ser.SerialReadString()
        if msg=="UID":
            # print("UID:")
            UID = interf.get_UID()
            UID_str = UID[2:]
            bytes_object = bytes.fromhex(UID_str)
            ascii_string = bytes_object.decode("ASCII")
            ascii_string = ascii_string.zfill(8)
            print(asciiCOM_string)
            # point.add_UID(ascii_string)
            # print("CurrentScore : ",point.getCurrentScore())
        elif msg!="":
            print(msg)

'''
def main():
    maze = mz.Maze(".\sample_code\sample_code\python\data\E_maze.csv")
    # point = score.Scoreboard("UID.csv", "team_NTUEE","http://140.112.175.15:3000")
    interf = interface.interface()
    
    readThread = threading.Thread(target=read)
    readThread.daemon = True
    readThread.start()
    # TODO : Initialize necessary variables
    interf.send_action(maze,1,6)
    time.sleep(0.05)
    interf.start()
    
    # #if (sys.argv[1] == '0'):
    #     print("Mode 0: for treasure-hunting")
    #     # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        
    # elif (sys.argv[1] == '1'):
    #     print("Mode 1: Self-testing mode.")
    #     # TODO: You can write your code to test specific function.#
'''

if __name__ == '__main__':
    maze = mz.Maze("medium_maze.csv")
    
    interf = interface.interface()
    mode = 1

    readThread = threading.Thread(target=read)
    readThread.daemon = True
    readThread.start()

    # TODO : Initialize necessary variables
    interf.send_action(maze,1,9,mode)
    time.sleep(1.5)
    
    # point = score.Scoreboard("UID.csv", "三上6","http://140.112.175.15:3000")
    # time.sleep(1)
    
    
    interf.start()
    
    while True:
        msgWrite = input()
        if msgWrite == "exit": sys.exit()
        interf.ser.SerialWrite(msgWrite)