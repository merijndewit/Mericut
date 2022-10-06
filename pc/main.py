import customtkinter
import atexit

#mericut
import TkinterRelated.Frames as Frames
from Serial import Serial

from TkinterRelated.Colors import Colors
from Serial import Serial
from microGcode.CallbackMicroGcode import CallbackMicroGcode
from microGcode.FileToMicroGcode import FileToMicroGcode

class Main(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        self.geometry("800x480")
        self.configure(bg=Colors.BGCOLOR)
        self.title("Mericut")
        self.terminating = False

        self.callbackMicroGcode = CallbackMicroGcode(self)
        self.serial = Serial(self)
        self.connectFrame = Frames.ConnectFrame(self, self)
        self.microGcodeFrame = Frames.MicroGcodeTestFrame(self, self)

        FileToMicroGcode.GetMicroGcodeFromTxt()

        self.mainloop();

    def OnExit(self):
        self.terminating = True
        
if __name__ == "__main__":
    main = Main()
    atexit.register(main.OnExit)