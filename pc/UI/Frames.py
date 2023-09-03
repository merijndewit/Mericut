import customtkinter
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image  

from UI.Colors import Colors

class LeftFramesContainer(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=400,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky=tkinter.NSEW, rowspan=5)
        self.columnconfigure(2, weight=1)
        