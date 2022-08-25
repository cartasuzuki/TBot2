from pyfirmata import Arduino, util
 #

class BraccioInterface:
  def __init__(self):
    #self.board = Arduino('/dev/ttyACM0')
    print("ccc")

  def setX(self, x):
        #commandstring = "x" + str(x) + "\0"
        #self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))
        print(x)
  def setY(self, y):
        commandstring = "y" + str(y)  + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))

  def setZ(self, z):
        commandstring = "z" + str(z) + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))


  def moveBraccio(self):
        commandstring = "cmd move" + "\0"
        self.board.send_sysex(0x71, util.str_to_two_byte_iter(commandstring))

  def setXYZ (self, x, y, z):
        self.setX(x)
        #self.setY(y)
        #self.setZ(z)

        


braccio = BraccioInterface()

braccio.setXYZ(100, 200, 300)


