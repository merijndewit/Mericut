from serial.tools import list_ports
import serial
import time
import threading
from MeriCode.FileToMeriCode import FileToMeriCode

class Serial:
    @staticmethod
    def GetPortNames():
        comList = list(list_ports.comports())
        nameList = []
        for i in range(len(comList)):
            nameList.append(comList[i].name)
        return nameList

    def __init__(self, parent):
        self.selectedComPort = None
        self.connectedDevice = None
        self.parent = parent
        self.fileIndex = 0
        self.file = FileToMeriCode.GetMeriCodeFromTxt()

    def Connect(self):
        if self.selectedComPort == None:
            return 
        self.connectedDevice = serial.Serial(port=self.selectedComPort, baudrate=115200, timeout=.1)
        self.StartListeningToSerial()

    def TestConnection(self):
        self.WriteToSerial("<D0>")

    def WriteToSerial(self, string):
        self.connectedDevice.write(bytes(string, 'utf-8'))

    def StartListeningToSerial(self):
        self.child_thread = threading.Thread(target=self.ListenToSerial, daemon=True)
        self.child_thread.start()
    
    def StartSendingMeriCodeList(self):
        self.WriteToSerial(self.file[0])
        self.fileIndex = 1

    def SendMeriCodeList(self):
        self.WriteToSerial(self.file[self.fileIndex])
        self.fileIndex += 1


    def ListenToSerial(self):
        while True:

            time.sleep(.1)
            try:
                if(self.connectedDevice.in_waiting > 0):
                    serialString = self.connectedDevice.readline()
                    string = serialString.decode('Ascii')
                    print("Arduino: " + string)
                    start = '<'
                    end = '>'
                    self.parent.callbackMeriCode.ExecuteCallbackCode(string[string.find(start)+len(start):string.rfind(end)])
                    
            except:
                self.parent.connectFrame.SetConnectionStatus(False)    
                return

                
        
