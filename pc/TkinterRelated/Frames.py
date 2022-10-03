import customtkinter
import tkinter
from TkinterRelated.Colors import Colors

class ConnectFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=0, column=0, padx=(0, 0), pady=(5, 0), sticky=tkinter.NE)
        self.grid_propagate(0)

        def ComPortSelected(choice):
            print("optionmenu dropdown clicked:", choice)

        self.comPortOption = customtkinter.CTkOptionMenu(master=self,
                                            values=["2", "1"],
                                            command=ComPortSelected)
        
        self.comPortOption.grid(row=1, column=0, sticky=tkinter.N)
        self.comPortOption.grid(row=1, column=0, sticky=tkinter.NE)


        self.previewButton = customtkinter.CTkButton(master=self, text="↻",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=25, height=25)
        self.previewButton.grid(row=1, column=1, sticky=tkinter.NE)


        self.previewButton = customtkinter.CTkButton(master=self, text="Connect",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=60, height=25)
        self.previewButton.grid(row=2, column=0, padx=(10, 10), pady=(5, 10))
