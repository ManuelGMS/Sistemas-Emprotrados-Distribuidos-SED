import serial
from time import sleep

class DaoConnection:
    
    def __init__(self):

        try:

            self.serialPort = serial.Serial('/dev/ttyACM0', 9600, timeout = 5)
            sleep(1) # Para que la comunicación se estaclezca correctamente.

        except Exception as ex:

            self.serialPort = None

    def __del__(self):

        try:

            self.serialPort.close()

        except Exception as ex:

            pass

    def writeConfigInSerial(self, config):

            try:

                self.serialPort.write(config["encoder"])
                self.serialPort.write(config["code"])
                self.serialPort.write(config["decoder"])
                self.serialPort.write(config["clues"])
                self.serialPort.write(config["sounds"])
                self.serialPort.write(config["answer"])
                self.serialPort.write(config["memory"])
                self.serialPort.write(config["rounds"])
                self.serialPort.write(config["match"]["round"])

                return True

            except Exception as ex:

                return False

    def readDataFromSerial(self):
        
        i = 0
        data = ""
        match = dict()
        match["round"] = 0
        match["results"] = []
        match["selections"] = []

        try:
        
            while data != "end":
            
                i += 1

                while(self.serialPort.in_waiting == 0):
                    pass

                data = self.serialPort.readline().decode('utf-8').strip()

                if data != "end":

                    if i == 1:
                        match["round"] = int(data)
                    elif i == 2:
                        match["selections"].append(data)
                    elif i == 3:
                        match["results"].append(data)
                        i = 0

            return None

        except Exception as ex:

            return match
