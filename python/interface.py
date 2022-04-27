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

    def send_action(self, mz,nd_from, nd_to,mode):
        # TODO : send the action to car
        # print("hi")
        if mode==0:
            self.action = mz.getAction(nd_from, nd_to)
        elif mode==1:
            self.action = mz.getTotalAction()
        elif mode ==2:
            self.action = mz.getTotalAction_2()
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
    it.send_action(mz,6,3)