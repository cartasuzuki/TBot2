import time
from pyfirmata import Arduino, util
 #

class BraccioInterface:
  def __init__(self):
    self.board = Arduino('/dev/ttyACM0')
    

  def setX(self, x):
        commandstring = "x" + str(x) + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))
        print(util.str_to_two_byte_iter(commandstring))
        time.sleep(1)
        
  def setY(self, y):
        commandstring = "y" + str(y)  + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))
        time.sleep(1)

  def setZ(self, z):
        commandstring = "z" + str(z) + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))
        print(util.str_to_two_byte_iter(commandstring))
        time.sleep(1)

  def setGripper(self, g):
        commandstring = "g" + str(g) + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))
        print(util.str_to_two_byte_iter(commandstring))
        time.sleep(1)

  def setWrist(self, w):
        commandstring = "w" + str(w) + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))
        print(util.str_to_two_byte_iter(commandstring))
        time.sleep(1)    

  def moveBraccio(self):
        commandstring = "cmd move" + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))
        time.sleep(1)

  def printXYZ(self):
        commandstring = "print XYZ" + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))
        time.sleep(1)

  def moveToXYZ (self, x, y, z):
        self.setX(x)
        self.setY(y)
        self.setZ(z)

        time.sleep(2)
        self.moveBraccio()


#end BraccioInterface class        


braccio = BraccioInterface()

braccio.setX(100)
time.sleep(5)

braccio.setY(200)
time.sleep(5)

braccio.setZ(300)
time.sleep(5)

braccio.printXYZ()

braccio.moveBraccio()

