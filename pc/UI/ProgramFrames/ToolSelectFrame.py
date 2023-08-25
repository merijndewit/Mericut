import customtkinter
import tkinter
import os

from PIL import ImageTk, Image  
from tkinter import filedialog

from UI.Colors import Colors

class ToolSelect(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=480,
                        height=28,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=1, column=1, padx=(0, 0), pady=(5, 0), sticky=tkinter.NW)
        self.grid_propagate(0)
        self.filename = ""

        self.lastDisabledButton = None
        from UI.DrawingTools import Pen, Move, QuadraticBezier, CubicBezier, Arc
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        moveImage = Image.open(os.path.dirname(os.path.dirname(dname)) + "/images/Select.png")
        moveImage = moveImage.resize((32, 32))
        tkinterMoveImage = ImageTk.PhotoImage(moveImage)

        self.moveButton = customtkinter.CTkButton(master=self, image=tkinterMoveImage, text="", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.moveButton.configure(command= lambda: self.SelectTool(Move, self.moveButton))
        self.moveButton.grid(row=0, column=0, sticky=tkinter.W)

        lineImage = Image.open(os.path.dirname(os.path.dirname(dname)) + "/images/Line.png")
        lineImage = lineImage.resize((32, 32))
        tkinterLineImage = ImageTk.PhotoImage(lineImage)
        
        self.penButton = customtkinter.CTkButton(master=self, image=tkinterLineImage, text="", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.penButton.configure(command= lambda: self.SelectTool(Pen, self.penButton))
        self.penButton.grid(row=0, column=1, sticky=tkinter.W)

        qBezierImage = Image.open(os.path.dirname(os.path.dirname(dname)) + "/images/Qbezier.png")
        qBezierImage = qBezierImage.resize((32, 32))
        tkinterqBezierImage = ImageTk.PhotoImage(qBezierImage)

        self.bezierButton = customtkinter.CTkButton(master=self, image=tkinterqBezierImage, text="", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.bezierButton.configure(command= lambda: self.SelectTool(QuadraticBezier, self.bezierButton))
        self.bezierButton.grid(row=0, column=2, sticky=tkinter.W)

        cBezierImage = Image.open(os.path.dirname(os.path.dirname(dname)) + "/images/Cbezier.png")
        cBezierImage = cBezierImage.resize((32, 32))
        tkinterqBezierImage = ImageTk.PhotoImage(cBezierImage)

        self.cubicBezierButton = customtkinter.CTkButton(master=self, image=tkinterqBezierImage, text="", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.cubicBezierButton.configure(command= lambda: self.SelectTool(CubicBezier, self.cubicBezierButton))
        self.cubicBezierButton.grid(row=0, column=3, sticky=tkinter.W)

        arcImage = Image.open(os.path.dirname(os.path.dirname(dname)) + "/images/Arc.png")
        arcImage = arcImage.resize((32, 32))
        tkinterArcImage = ImageTk.PhotoImage(arcImage)

        self.arcButton = customtkinter.CTkButton(master=self, image=tkinterArcImage, text="", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.arcButton.configure(command= lambda: self.SelectTool(Arc, self.arcButton))
        self.arcButton.grid(row=0, column=4, sticky=tkinter.W)

        self.saveSVGButton = customtkinter.CTkButton(master=self, text="Save SVG", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.SaveSVG())
        self.saveSVGButton.grid(row=0, column=6, sticky='e')

        self.fileSelecting = customtkinter.CTkButton(master=self, text="Load SVG", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: self.SelectFile())
        self.fileSelecting.grid(row=0, column=7, sticky='e')

        self.SelectTool(Move, self.moveButton)


    def SelectFile(self):
        filetypes = (('svg files', '*.svg'), ('All files', '*.*'))
        self.filename = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        self.parent.canvas.canvas.LoadSVG(self.filename)

    def SelectTool(self, name, button):
        if button == self.lastDisabledButton:
            return
        if self.lastDisabledButton != None:
            self.lastDisabledButton.configure(state=tkinter.NORMAL, fg_color=Colors.BUTTONNOTSELECTED)

        button.configure(state=tkinter.DISABLED, fg_color=Colors.BUTTON)
        self.lastDisabledButton = button
        self.parent.canvas.canvas.SetTool(name)