import customtkinter
import tkinter

from UI.Colors import Colors

class MeriCodeTestFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=1, column=0, padx=(0, 0), pady=(5, 0), sticky=tkinter.NW)
        self.grid_propagate(0)

        self.entry = customtkinter.CTkEntry(master=self, placeholder_text="MeriCode", width=120, height=25, border_width=2, corner_radius=10, text_color=Colors.BUTTONTEXT)
        self.entry.grid(row=0, column=0, sticky=tkinter.NW, columnspan=2)
        
        self.submitButton = customtkinter.CTkButton(master=self, text=">",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: SendEntryString())
        self.submitButton.grid(row=0, column=2, sticky=tkinter.NW)

        def SendEntryString():
            self.parent.serial.WriteToSerial(self.entry.get())