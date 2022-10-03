from serial.tools import list_ports
import serial
import time

class Serial:
    def GetPortNames():
        comList = list(list_ports.comports())
        nameList = []
        for i in range(len(comList)):
            nameList.append(comList[i].name)
        return nameList

    def __init__(self):
        self.selectedComPort = None
        self.connectedDevice = None

    def Connect(self):
        if self.selectedComPort == None:
            return
        self.connectedDevice = serial.Serial(port=self.selectedComPort, baudrate=115200, timeout=.1)

    def TestConnection(self):
        callback = self.WriteToSerial("<D0>")
        print(callback)

    def WriteToSerial(self, string):
        self.connectedDevice.write(bytes(string, 'utf-8'))
        time.sleep(0.05)
        data = self.connectedDevice.readline()
        return data
        
