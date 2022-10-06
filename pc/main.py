import customtkinter
import atexit

#mericut
import TkinterRelated.Frames as Frames
from Serial import Serial

from TkinterRelated.Colors import Colors
from Serial import Serial
from MeriCode.CallbackMeriCode import CallbackMeriCode
from MeriCode.FileToMeriCode import FileToMeriCode

class Main(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        self.geometry("800x480")
        self.configure(bg=Colors.BGCOLOR)
        self.title("Mericut")
        self.terminating = False

        self.callbackMeriCode = CallbackMeriCode(self)
        self.serial = Serial(self)
        self.connectFrame = Frames.ConnectFrame(self, self)
        self.MeriCodeFrame = Frames.MeriCodeTestFrame(self, self)

        FileToMeriCode.GetMeriCodeFromTxt()

        self.mainloop();

    def OnExit(self):
        self.terminating = True
        
if __name__ == "__main__":
    main = Main()
    atexit.register(main.OnExit)