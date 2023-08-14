import customtkinter
import tkinter

from UI.Colors import Colors

class MeriCodeFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=2, column=0, padx=(0, 0), pady=(5, 0), sticky=tkinter.NW)
        self.grid_propagate(0)
        self.cutting = False
        self.line = 0

        self.drawingText = customtkinter.CTkLabel(master=self, text="Drawing", text_color=Colors.TEXT, font=("", 11), anchor=tkinter.W, width=60)
        self.drawingText.grid(row=0, column=0, sticky=tkinter.W)

        self.slicingSwitch = customtkinter.CTkSwitch(master=self, text="", command= lambda: self.Switched(), progress_color=Colors.BUTTON, button_color=Colors.BGSECCOLOR)
        self.slicingSwitch.grid(row=0, column=1, sticky=tkinter.W)
        
        self.cuttingText = customtkinter.CTkLabel(master=self, text="Cutting", text_color=Colors.TEXT, font=("", 11), anchor=tkinter.W)
        self.cuttingText.grid(row=0, column=2, sticky=tkinter.W)

        self.submitButton = customtkinter.CTkButton(master=self, text="Generate MeriCode",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, font=("", 11), width=200, height=50, text_color=Colors.BUTTONTEXT, command= lambda: self.GenerateMeriCode())
        self.submitButton.grid(row=1, column=0, columnspan=5, sticky=tkinter.SW)

        self.showButton = customtkinter.CTkButton(master=self, text="<",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, font=("", 11), width=25, height=25, text_color=Colors.BUTTONTEXT, command= lambda: self.ShowNextLine(-1))
        self.showButton.grid(row=2, column=0, sticky=tkinter.W)

        self.showButton = customtkinter.CTkButton(master=self, text="Show MeriCode",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, font=("", 11), width=125, height=25, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.ShowMeriCode(self.cutting))
        self.showButton.grid(row=2, column=0, columnspan=2, padx=(30, 5), sticky=tkinter.W)

        self.showButton = customtkinter.CTkButton(master=self, text=">",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, font=("", 11), width=25, height=25, text_color=Colors.BUTTONTEXT, command= lambda: self.ShowNextLine(1))
        self.showButton.grid(row=2, column=2, sticky=tkinter.W)

    def Switched(self):
        if self.slicingSwitch.get() == 0:
            self.parent.mericodeSlicingOptions.cutting = False
        else:
            self.parent.mericodeSlicingOptions.cutting = True

    def GenerateMeriCode(self):
        self.parent.canvas.canvas.CanvasToMeriCode(self.cutting)
        canvasToMericode = self.parent.canvas.canvas.canvasToMericode
        self.parent.mericodeInfo.setAmountOfLines(canvasToMericode.lines)
        self.parent.mericodeInfo.setAmountOfTravels(canvasToMericode.travels)
        self.parent.mericodeInfo.setAmountOfShapes(canvasToMericode.shapes)

    def ShowNextLine(self, incresement):
        self.parent.canvas.canvas.ShowSingleMeriCodeLine(self.line)
        self.line += incresement
