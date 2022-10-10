import tkinter
from UI.Colors import Colors
import UI.CanvasTools as CanvasTools

class DrawingCanvas(tkinter.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure( width=590,
                        height=590,
                        highlightthickness=0,
                        bg=Colors.CANVASBACKGROUND)

        self.bind("<Button-1>", self.Clicked)

        CanvasTools.DrawGrid(self, 59)

    def Clicked(self, event):
        return