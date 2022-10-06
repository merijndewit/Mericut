class CallbackMicroGcode:
    def __init__(self, parent):
        self.parent = parent

    def ExecuteCallbackCode(self, callbackCode):
        if callbackCode[0] == 'E':
            self.ExecuteEcode(callbackCode[1:])
        elif callbackCode[0] == 'C':
            self.ExecuteCcode(callbackCode[1:])

    def ExecuteEcode(self, callbackCode):
        if callbackCode[0] == '0':
            return    
        elif callbackCode[0] == '1':
            return

    def ExecuteCcode(self, callbackCode):
        if callbackCode[0] == '0':
            self.parent.connectFrame.SetConnectionStatus(True)    
        elif callbackCode[0] == '1':
            return
            