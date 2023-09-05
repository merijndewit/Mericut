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
from MeriCode.MericodeSlicingOptions import MericodeSlicingOptions

class Main(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        self.geometry("820x520")
        self.configure(fg_color=Colors.BGSECCOLOR)
        self.title("Mericut")
        self.terminating = False

        self.serial = Serial(self)
        self.callbackMeriCode = CallbackMeriCode(self)
        self.mericodeSlicingOptions = MericodeSlicingOptions()

        #Frames
        leftFramesContainer = Frames.LeftFramesContainer(self, self)
        self.headerFrame = HeaderFrame.HeaderFrame(self, self)
        self.connectFrame = ConnectFrame.ConnectFrame(self, leftFramesContainer)
        self.meriCodeTestFrame = MericodeTestFrame.MeriCodeTestFrame(self, leftFramesContainer)
        self.meriCodeFrame = MeriCodeFrame.MeriCodeFrame(self, leftFramesContainer)
        self.hardwareAcceleratedCanvas = Canvas.HardwareAcceleratedCanvas(self, self)
        self.toolSelect = ToolSelect.ToolSelect(self, self)
        self.backgroundFrame = BackgroundFrame.BackgroundFrame(self, self)
        self.canvasLayerFrame = CanvasLayerFrame.CanvasLayerFrame(self, self)
        self.mericodeInfo = MeriCodeInfoFrame.MericodeInfo(self, self)

        FileToMeriCode.GetMeriCodeFromTxt()
        self.update()
        self.hardwareAcceleratedCanvas.pygame.display.update()

        self.hardwareAcceleratedCanvas.InitializeDisplay()
        self.Run()
        

    def OnExit(self):
        self.terminating = True

    def Run(self):
        while True:
            self.update()

            self.hardwareAcceleratedCanvas.pygame.display.update()

        
if __name__ == "__main__":
    main = Main()
    atexit.register(main.OnExit)
