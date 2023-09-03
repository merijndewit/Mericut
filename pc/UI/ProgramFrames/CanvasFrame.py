import customtkinter
import tkinter

from UI.Colors import Colors
from UI.TkCanvasFrame import DrawingCanvas


class Canvas(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=600,
                        height=600,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), rowspan=4, sticky=tkinter.NSEW)
        self.parent.columnconfigure(1, weight=1)
        self.parent.rowconfigure(5, weight=1)
        self.canvas = DrawingCanvas(self)
        self.canvas.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky=tkinter.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)