import customtkinter
import atexit

#mericut
import UI.Frames as Frames

import UI.ProgramFrames.HeaderFrame as HeaderFrame
import UI.ProgramFrames.ConnectFrame as ConnectFrame
import UI.ProgramFrames.MericodeTestFrame as MericodeTestFrame
import UI.ProgramFrames.MeriCodeFrame as MeriCodeFrame
import UI.ProgramFrames.ToolSelectFrame as ToolSelect
import UI.ProgramFrames.CanvasFrame as Canvas
import UI.ProgramFrames.CanvasLayerFrame as CanvasLayerFrame
import UI.ProgramFrames.BackgroundFrame as BackgroundFrame
import UI.ProgramFrames.MericodeInfoFrame as MeriCodeInfoFrame

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
        self.headerFrame = HeaderFrame.HeaderFrame(self, self)
        self.connectFrame = ConnectFrame.ConnectFrame(self, leftFramesContainer)
        self.meriCodeTestFrame = MericodeTestFrame.MeriCodeTestFrame(self, leftFramesContainer)
        self.meriCodeFrame = MeriCodeFrame.MeriCodeFrame(self, leftFramesContainer)
        self.canvas = Canvas.Canvas(self, self)
        self.toolSelect = ToolSelect.ToolSelect(self, self)
        self.backgroundFrame = BackgroundFrame.BackgroundFrame(self, self)
        self.canvasLayerFrame = CanvasLayerFrame.CanvasLayerFrame(self, self)
        self.mericodeInfo = MeriCodeInfoFrame.MericodeInfo(self, self)


        FileToMeriCode.GetMeriCodeFromTxt()

        self.mainloop()

    def OnExit(self):
        self.terminating = True
        
if __name__ == "__main__":
    main = Main()
    atexit.register(main.OnExit)