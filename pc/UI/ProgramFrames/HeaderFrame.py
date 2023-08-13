import customtkinter
from UI.Colors import Colors
from PIL import ImageTk, Image  
import tkinter

class HeaderFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=40,
                        corner_radius=4,
                        fg_color=Colors.BGHEADERFRAME)

        self.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky=tkinter.NSEW, columnspan=3)
        self.columnconfigure(2, weight=1)
        self.grid_propagate(0)

        self.header = customtkinter.CTkLabel(master=self, text="MeriCut", text_color=Colors.TEXT, font=("", 11), anchor=tkinter.W)
        self.header.grid(row=0, column=2, sticky=tkinter.NW, pady=(6, 0))

        logo = Image.open("images/logo.png")
        logo = logo.resize((40, 40))
        tkinterLogo = ImageTk.PhotoImage(logo)
        self.button = customtkinter.CTkButton(master=self, image=tkinterLogo, text="", fg_color=Colors.BGHEADERFRAME, hover_color=Colors.BGHEADERFRAME, font=("", 11), width=40, height=40, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.serial.TestConnection())  # type: ignore
        self.button.grid(row=0, column=0, sticky=tkinter.W, padx=(5, 5))