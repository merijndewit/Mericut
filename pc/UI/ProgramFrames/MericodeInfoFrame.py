import customtkinter
import tkinter

from UI.Colors import Colors

class MericodeInfo(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=100,
                        corner_radius=4,
                        fg_color=Colors.BGCOLOR)
        
        self.grid(row=4, column=2, padx=(5, 5), pady=(5, 5), rowspan=1, sticky=tkinter.NSEW)
        self.grid_propagate(False)

        self.linesText = customtkinter.CTkLabel(master=self, text="Number of lines: ", text_color=Colors.TEXT, font=("", 11), anchor=tkinter.W)
        self.linesText.grid(row=0, column=0, sticky=tkinter.NW, columnspan=1, padx=(5, 0))

        self.travelsText = customtkinter.CTkLabel(master=self, text="Number of travels: ", text_color=Colors.TEXT, font=("", 11), anchor=tkinter.W)
        self.travelsText.grid(row=1, column=0, sticky=tkinter.NW, columnspan=1, padx=(5, 0))

        self.amountOfLinesText = customtkinter.CTkLabel(master=self, text="-", text_color=Colors.TEXT, font=("", 11), anchor=tkinter.W)
        self.amountOfLinesText.grid(row=0, column=1, sticky=tkinter.NW, columnspan=1, padx=(5, 0))

        self.amountOfTravels = customtkinter.CTkLabel(master=self, text="-", text_color=Colors.TEXT, font=("", 11), anchor=tkinter.W)
        self.amountOfTravels.grid(row=1, column=1, sticky=tkinter.NW, columnspan=1, padx=(5, 0))

    def setAmountOfLines(self, number):
        self.amountOfLinesText.configure(text=number)

    def setAmountOfTravels(self, number):
        self.amountOfTravels.configure(text=number)