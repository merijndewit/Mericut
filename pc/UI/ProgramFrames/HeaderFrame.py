import customtkinter
from UI.Colors import Colors
from PIL import ImageTk, Image  
import tkinter
import os

class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=48,
                        corner_radius=0,
                        fg_color=Colors.BGHEADERFRAME)

        self.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky=tkinter.NSEW, columnspan=3)
        self.columnconfigure(2, weight=1)
        self.grid_propagate(0)

        self.header = customtkinter.CTkLabel(master=self, text="MeriCut", text_color=Colors.TEXT, font=("Arial Bold", 21), anchor=tkinter.W)
        self.header.grid(row=0, column=2, sticky=tkinter.NW, pady=(6, 0))
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        logo = Image.open(os.path.dirname(os.path.dirname(dname)) + "/images/logo.png")
        tkinterLogo = customtkinter.CTkImage(logo, size=(38, 38))
        self.button = customtkinter.CTkButton(master=self, image=tkinterLogo, text="", fg_color=Colors.BGHEADERFRAME, hover_color=Colors.BGHEADERFRAME, width=45, height=45, text_color=Colors.BUTTONTEXT)  # type: ignore
        self.button.grid(row=0, column=0, sticky=tkinter.W, padx=(5, 5))