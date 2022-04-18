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
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
        input("Press enter to start.")
        self.ser.SerialWrite('s')

    def get_UID(self):
        return self.ser.SerialReadByte()

    def send_action(self, mz, nd_from, nd_to):
        # TODO : send the action to car
        self.action = mz.getAction(nd_from, nd_to)
        print (self.action)
        for i in range (len(self.action)):
            self.ser.SerialWrite(self.action[i])

    def end_process(self):
        self.ser.SerialWrite('e')
        self.ser.disconnect()

if __name__ == '__main__':
    it = interface()
    mz = maze("medium_maze.csv")
    it.send_action(mz,12,3)
    