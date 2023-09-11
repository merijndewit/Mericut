import customtkinter
import atexit
import time
import sys
import threading

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

import UI.CanvasManager as CanvasManager

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


        #Frames / UI
        leftFramesContainer = Frames.LeftFramesContainer(self, self)
        self.headerFrame = HeaderFrame.HeaderFrame(self, self)
        self.connectFrame = ConnectFrame.ConnectFrame(self, leftFramesContainer)
        self.meriCodeTestFrame = MericodeTestFrame.MeriCodeTestFrame(self, leftFramesContainer)
        self.meriCodeFrame = MeriCodeFrame.MeriCodeFrame(self, leftFramesContainer)
        self.backgroundFrame = BackgroundFrame.BackgroundFrame(self, self)
        self.mericodeInfo = MeriCodeInfoFrame.MericodeInfo(self, self)
        self.hardwareAcceleratedCanvas = Canvas.HardwareAcceleratedCanvas(self, self)
        self.hardwareAcceleratedCanvas.InitializeDisplay()
        
        self.canvasManager = CanvasManager.CanvasManager(self)

        self.canvasLayerFrame = CanvasLayerFrame.CanvasLayerFrame(self, self)
        self.toolSelect = ToolSelect.ToolSelect(self, self)

        self.hardwareAcceleratedCanvas.SendEventsToCanvas(self.canvasManager)
        
    def StartRenderThreadLoop(self):
        while not self.terminating:
            self.hardwareAcceleratedCanvas.UpdateCanvas()

    def OnExit(self):
        self.terminating = True
        self.hardwareAcceleratedCanvas.pygame.quit()
        exit()

def Stop():
    print("Stopping")
    return

atexit.register(Stop)

def SecondInit():
    main.hardwareAcceleratedCanvas.canvas.CanvasChanged()
        
if __name__ == "__main__":
    main = Main()
    
    renderThread = threading.Thread(target=main.StartRenderThreadLoop, daemon=True)
    renderThread.start()

    main.after(100, SecondInit)
    main.mainloop()
