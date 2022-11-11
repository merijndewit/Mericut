import customtkinter
import atexit

#mericut
import UI.Frames as Frames
from Serial import Serial

from UI.Colors import Colors
from Serial import Serial
from MeriCode.CallbackMeriCode import CallbackMeriCode
from MeriCode.FileToMeriCode import FileToMeriCode

class Main(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        self.geometry("820x520")
        self.configure(bg=Colors.BGCOLOR)
        self.title("Mericut")
        self.terminating = False

        leftFramesContainer = Frames.LeftFramesContainer(self, self)
        self.callbackMeriCode = CallbackMeriCode(self)
        self.serial = Serial(self)
        self.headerFrame = Frames.HeaderFrame(self, self)
        self.connectFrame = Frames.ConnectFrame(self, leftFramesContainer)
        self.MeriCodeFrame = Frames.MeriCodeTestFrame(self, leftFramesContainer)
        self.meriCodeFrame = Frames.MeriCodeFrame(self, leftFramesContainer)
        self.canvas = Frames.Canvas(self, self)
        self.toolSelect = Frames.ToolSelect(self, self)
        self.backgroundFrame = Frames.BackgroundFrame(self, self)
        self.canvasLayerFrame = Frames.CanvasLayerFrame(self, self)


        FileToMeriCode.GetMeriCodeFromTxt()

        self.mainloop();

    def OnExit(self):
        self.terminating = True
        
if __name__ == "__main__":
    main = Main()
    atexit.register(main.OnExit)