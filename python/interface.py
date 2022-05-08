import BT
import maze 
import score

# hint: You may design additional functions to execute the input command, which will be helpful when debugging :)

class interface:
    def __init__(self):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        port = input("PC bluetooth port name: ")
        self.port = port
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
        

    def get_UID(self):
        return self.ser.SerialReadByte()

    def send_action(self, mz,nd_from, nd_to,r_time,mode):
        '''
        ## send the action to car\n
        Mode 0 : getAction from A to B
        Mode 1 : getTotalAction
        Mode 2 : go to the furthest end point then alone the path get into 2 step end point
        Mode 3 : getTotalAction with consideration of time bias
        Mode 4 : read action from file 'path.txt'
        '''
        if mode==0:
            self.action = mz.getAction(nd_from, nd_to)
        elif mode==1:
            self.action = mz.getTotalAction()
        elif mode ==2:
            self.action = mz.getTotalAction_2()
        elif mode == 3:
            self.action = mz.getTotalAction_3(r_time)
        elif mode == 4:
            self.action = []
            path = 'path.txt'
            with open(path) as f:
                for line in f.readlines():
                    s = line.split(' ')
                    self.action.append(s[0])
        print(self.action)
        for i in range (len(self.action)):
            self.ser.SerialWrite(self.action[i])

    def start(self):
        # input("Press enter to start.")
        self.ser.SerialWrite('s')

    def end_process(self):
        self.ser.SerialWrite('e')
        self.ser.disconnect()

if __name__ == '__main__':
    mz = maze.Maze("small_maze.csv")
    it = interface()
    it.send_action(mz,6,3,90,4)