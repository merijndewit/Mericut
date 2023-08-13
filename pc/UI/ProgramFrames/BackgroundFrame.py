import customtkinter
import tkinter

from UI.Colors import Colors

class BackgroundFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=300,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=1, column=2, padx=(5, 5), pady=(5, 5), rowspan=3, sticky=tkinter.NSEW)
        self.grid_propagate(False)

        self.header = customtkinter.CTkLabel(master=self, text="Backgrounds", text_color=Colors.TEXT, font=("", 11), anchor=tkinter.W)
        self.header.grid(row=0, column=0, sticky=tkinter.NW, columnspan=2, padx=(5, 0))

        self.moveButton = customtkinter.CTkButton(master=self, text="A4", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, font=("", 13), width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.SetBackground("A4"))
        self.moveButton.grid(row=1, column=0, sticky=tkinter.NW)

        self.moveButton = customtkinter.CTkButton(master=self, text="A5", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, font=("", 13), width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.SetBackground("A5"))
        self.moveButton.grid(row=1, column=1, sticky=tkinter.NW)

        self.moveButton = customtkinter.CTkButton(master=self, text="A6", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, font=("", 13), width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.SetBackground("A6"))
        self.moveButton.grid(row=1, column=2, sticky=tkinter.NW)