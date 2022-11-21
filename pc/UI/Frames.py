from cgitb import text
import customtkinter
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image  

from UI.Colors import Colors
from Serial import Serial
from UI.DrawingCanvas import DrawingCanvas

class LeftFramesContainer(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=400,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky=tkinter.NSEW, rowspan=5)
        self.columnconfigure(2, weight=1)

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

        self.header = customtkinter.CTkLabel(master=self, text="MeriCut", text_color=Colors.TEXT, text_font='Helvetica 13 bold', anchor=tkinter.W)
        self.header.grid(row=0, column=2, sticky=tkinter.NW, pady=(6, 0))

        logo = Image.open("images/logo.png")
        logo = logo.resize((40, 40), Image.ANTIALIAS)
        tkinterLogo = ImageTk.PhotoImage(logo)
        self.button = customtkinter.CTkButton(master=self, image=tkinterLogo, text="", fg_color=Colors.BGHEADERFRAME, hover_color=Colors.BGHEADERFRAME, text_font=("", 11), width=40, height=40, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.serial.TestConnection())  # type: ignore
        self.button.grid(row=0, column=0, sticky=tkinter.W, padx=(5, 5))

class ConnectFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky=tkinter.NW)
        self.grid_propagate(0)

        def ComPortSelected(choice):
            self.parent.serial.selectedComPort = choice

        self.connectionStatusText = customtkinter.CTkLabel(master=self, text="Status: ", text_color=Colors.TEXT, text_font='Helvetica 11 bold', anchor=tkinter.W)
        self.connectionStatusText.grid(row=1, column=0, sticky=tkinter.NW, columnspan=2)

        self.connectionStatus = customtkinter.CTkLabel(master=self, text_font='Helvetica 11 bold')
        self.connectionStatus.grid(row=1, column=1, sticky=tkinter.NW, columnspan=2)
        self.SetConnectionStatus(False)

        def SetAvailableComPorts(comPorts):
            self.comPortOption.configure(values=comPorts)

        self.comPortOption = customtkinter.CTkOptionMenu(master=self, values=["Select port"], command=ComPortSelected, fg_color=Colors.BUTTON, button_color=Colors.BUTTON, button_hover_color=Colors.BUTTONHOVER, text_color=Colors.BUTTONTEXT)
        
        self.comPortOption.grid(row=2, column=0, sticky=tkinter.NW, columnspan=2)


        self.previewButton = customtkinter.CTkButton(master=self, text="↻",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: SetAvailableComPorts(Serial.GetPortNames()))
        self.previewButton.grid(row=2, column=2, sticky=tkinter.NW)

        self.connectButton = customtkinter.CTkButton(master=self, text="Connect",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=70, height=25, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.serial.Connect())
        self.connectButton.grid(row=3, column=0, sticky=tkinter.W)
        self.connectButton.grid_propagate(0)

        self.testConnectionButton = customtkinter.CTkButton(master=self, text="Test",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=70, height=25, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.serial.TestConnection())
        self.testConnectionButton.grid(row=3, column=1, sticky=tkinter.W)
        self.testConnectionButton.grid_propagate(0)

    def SetConnectionStatus(self, bool):
        if bool:
            self.connectionStatus.configure(text="Connected!", text_color=Colors.CONNECTEDTEXT)
            return
        self.connectionStatus.configure(text="Disconnected.", text_color=Colors.DISCONNECTEDTEXT)


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
        
        self.submitButton = customtkinter.CTkButton(master=self, text=">",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: SendEntryString())
        self.submitButton.grid(row=0, column=2, sticky=tkinter.NW)

        self.sendTestFile = customtkinter.CTkButton(master=self, text="Send File",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=100, height=28, text_color=Colors.BUTTONTEXT, command= lambda: StartSendingFile())
        self.sendTestFile.grid(row=1, column=0, sticky=tkinter.NW, columnspan=1)

        def StartSendingFile():
            self.parent.serial.LoadMeriCodeFile()
            self.parent.serial.SendMeriCodeList()

        def SendEntryString():
            self.parent.serial.WriteToSerial(self.entry.get())

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

        self.drawingText = customtkinter.CTkLabel(master=self, text="Drawing", text_color=Colors.TEXT, text_font='Helvetica 11', anchor=tkinter.W, width=60)
        self.drawingText.grid(row=0, column=0, sticky=tkinter.W)

        self.slicingSwitch = customtkinter.CTkSwitch(master=self, text="", command= lambda: self.Switched(), progress_color=Colors.BUTTON, button_color=Colors.BGSECCOLOR)
        self.slicingSwitch.grid(row=0, column=1, sticky=tkinter.W)
        
        self.cuttingText = customtkinter.CTkLabel(master=self, text="Cutting", text_color=Colors.TEXT, text_font='Helvetica 11', anchor=tkinter.W)
        self.cuttingText.grid(row=0, column=2, sticky=tkinter.W)

        self.submitButton = customtkinter.CTkButton(master=self, text="Generate MeriCode",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=200, height=50, text_color=Colors.BUTTONTEXT, command= lambda: self.GenerateMeriCode())
        self.submitButton.grid(row=1, column=0, columnspan=5, sticky=tkinter.SW)

    def Switched(self):
        if self.slicingSwitch.get() == 0:
            self.cutting = False
        else:
            self.cutting = True

    def GenerateMeriCode(self):
        self.parent.canvas.canvas.CanvasToMeriCode(self.cutting)

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

        self.penButton = customtkinter.CTkButton(master=self, text="Pen", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.penButton.configure(command= lambda: self.SelectTool(Pen, self.penButton))
        self.penButton.grid(row=0, column=0, sticky=tkinter.W)

        self.bezierButton = customtkinter.CTkButton(master=self, text="Q Bezier", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.bezierButton.configure(command= lambda: self.SelectTool(QuadraticBezier, self.bezierButton))
        self.bezierButton.grid(row=0, column=1, sticky=tkinter.W)

        self.cubicBezierButton = customtkinter.CTkButton(master=self, text="C Bezier", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.cubicBezierButton.configure(command= lambda: self.SelectTool(CubicBezier, self.cubicBezierButton))
        self.cubicBezierButton.grid(row=0, column=2, sticky=tkinter.W)

        self.arcButton = customtkinter.CTkButton(master=self, text="Arc", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.arcButton.configure(command= lambda: self.SelectTool(Arc, self.arcButton))
        self.arcButton.grid(row=0, column=3, sticky=tkinter.W)

        self.moveButton = customtkinter.CTkButton(master=self, text="Move", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.moveButton.configure(command= lambda: self.SelectTool(Move, self.moveButton))
        self.moveButton.grid(row=0, column=4, sticky=tkinter.W)

        self.loadSVGButton = customtkinter.CTkButton(master=self, text="Load SVG", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.LoadSVG(self.filename))
        self.loadSVGButton.grid(row=0, column=5, sticky='e')
        self.saveSVGButton = customtkinter.CTkButton(master=self, text="Save SVG", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.SaveSVG())
        self.saveSVGButton.grid(row=0, column=6, sticky='e')

        self.fileSelecting = customtkinter.CTkButton(master=self, text="..", fg_color=Colors.BUTTONNOTSELECTED, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: self.SelectFile())
        self.fileSelecting.grid(row=0, column=7, sticky='e')

        self.SelectTool(Pen, self.penButton)


    def SelectFile(self):
        filetypes = (('svg files', '*.svg'), ('All files', '*.*'))
        self.filename = filedialog.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)

    def SelectTool(self, name, button):
        if button == self.lastDisabledButton:
            return
        if self.lastDisabledButton != None:
            self.lastDisabledButton.configure(state=tkinter.NORMAL, fg_color=Colors.BUTTONNOTSELECTED)

        button.configure(state=tkinter.DISABLED, fg_color=Colors.BUTTON)
        self.lastDisabledButton = button
        self.parent.canvas.canvas.SetTool(name)

class Canvas(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=600,
                        height=600,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), rowspan=4, sticky=tkinter.NSEW)
        self.parent.columnconfigure(1, weight=1)
        self.parent.rowconfigure(5, weight=1)
        self.canvas = DrawingCanvas(self)
        self.canvas.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky=tkinter.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

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

        self.header = customtkinter.CTkLabel(master=self, text="Backgrounds", text_color=Colors.TEXT, text_font='Helvetica 11', anchor=tkinter.W)
        self.header.grid(row=0, column=0, sticky=tkinter.NW, columnspan=2, padx=(5, 0))

        self.moveButton = customtkinter.CTkButton(master=self, text="A4", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, text_font="Helvetica 13 bold", width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.SetBackground("A4"))
        self.moveButton.grid(row=1, column=0, sticky=tkinter.NW)

        self.moveButton = customtkinter.CTkButton(master=self, text="A5", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, text_font="Helvetica 13 bold", width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.SetBackground("A5"))
        self.moveButton.grid(row=1, column=1, sticky=tkinter.NW)

        self.moveButton = customtkinter.CTkButton(master=self, text="A6", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, text_font="Helvetica 13 bold", width=55, height=70, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.SetBackground("A6"))
        self.moveButton.grid(row=1, column=2, sticky=tkinter.NW)

class CanvasLayerFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=300,
                        corner_radius=4,
                        fg_color=Colors.BGCOLOR)

        self.grid(row=3, column=2, padx=(5, 5), pady=(5, 5), rowspan=3, sticky=tkinter.NSEW)
        self.grid_propagate(False)
        self.posX = 0
        self.posY = 1
        self.maxWidth = 3
        
        self.moveButton = customtkinter.CTkButton(master=self, text="+", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, text_font="Helvetica 13 bold", width=40, height=40, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.AddLayer())
        self.moveButton.grid(row=0, column=0, pady=(0, 5), sticky=tkinter.NW)

        layerNames = self.parent.canvas.canvas.GetLayerNames()
        self.layerFrames = []
        for i in range(len(layerNames)):
            self.AddLayerButton(layerNames[i])

            
    def AddLayerButton(self, name):
        layerFrame = LayerButtonFrame(self, self, name)
        layerFrame.grid(row=self.posY, column=self.posX, sticky=tkinter.NW)
        layerFrame.grid_propagate(False)
        self.layerFrames.append(layerFrame)
        self.posX += 1
        if self.posX == self.maxWidth:
            self.posX = 0
            self.posY += 1

class LayerButtonFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, name, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.name = name
        self.configure( width=60,
                        height=70,
                        corner_radius=4,
                        fg_color=Colors.PAPERBACKGROUND)

        self.grid(row=0, column=0, padx=(0, 5), pady=(5, 0), sticky=tkinter.NSEW)
        self.grid_propagate(False)
        self.button = customtkinter.CTkButton(master=self, text=name, fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, width=60, height=70, text_color=Colors.BUTTONTEXT, corner_radius=4, command= lambda: self.SelectLayer())
        self.button.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), rowspan=4, columnspan=3, sticky=tkinter.NSEW)

        self.selectbutton = customtkinter.CTkButton(master=self, text="↔", fg_color=Colors.BUTTON, hover_color=Colors.PAPERHOVERCOLOR, width=12, height=12, text_color=Colors.BUTTONTEXT, command= lambda: self.TransformLayer())
        self.selectbutton.grid(row=3, column=0, padx=(0, 0), pady=(0, 0), sticky=tkinter.SW)

    def SelectLayer(self):
        self.parent.parent.canvas.canvas.SelectLayer(self.name)

    def TransformLayer(self):
        self.parent.parent.canvas.canvas.TransformLayer(self.name)
