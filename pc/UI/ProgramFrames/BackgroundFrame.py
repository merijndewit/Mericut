import customtkinter
import tkinter

from UI.Colors import Colors

class BackgroundFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=320,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=1, column=2, padx=(5, 5), pady=(5, 5), rowspan=3, sticky=tkinter.NSEW)
        self.grid_propagate(False)

        row : int = 0

        self.header = customtkinter.CTkLabel(master=self, text="Backgrounds", text_color=Colors.TEXT, font=("Arial Bold", 11), anchor=tkinter.W)
        self.header.grid(row=row, column=0, sticky=tkinter.S, columnspan=4, padx=(5, 0))
        
        ########next row
        row += 1

        self.label = customtkinter.CTkLabel(master=self, text="", fg_color=Colors.SEPERATIONLINE, height=2)
        self.label.grid(row=row, column=0, sticky=tkinter.EW, columnspan=4, pady=(5, 5), padx=(5, 5))
        self.label.grid_propagate(False)

        ########next row
        row += 1

        self.moveButton = customtkinter.CTkButton(master=self, text="A4", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, font=("", 13), width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.SetBackground("A4"))
        self.moveButton.grid(row=row, column=0, sticky=tkinter.NW)

        self.moveButton = customtkinter.CTkButton(master=self, text="A5", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, font=("", 13), width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.SetBackground("A5"))
        self.moveButton.grid(row=row, column=1, sticky=tkinter.NW)

        self.moveButton = customtkinter.CTkButton(master=self, text="A6", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, font=("", 13), width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.SetBackground("A6"))
        self.moveButton.grid(row=row, column=2, sticky=tkinter.NW)