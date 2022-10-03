import customtkinter
import tkinter

class ConnectFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=120,
                        corner_radius=4,
                        fg_color="#1E1E1E")

        self.grid(row=1, column=0, padx=(0, 0), pady=(5, 0), sticky=tkinter.NE)
        self.grid_propagate(0)