from cgitb import text
import customtkinter
import tkinter

from UI.Colors import Colors
from Serial import Serial
from UI.DrawingCanvas import DrawingCanvas

class ConnectFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=300,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=0, column=0, padx=(0, 5), pady=(5, 0), sticky=tkinter.NE, rowspan=2)
        self.grid_propagate(0)

        def ComPortSelected(choice):
            self.parent.serial.selectedComPort = choice

        self.connectionStatusText = customtkinter.CTkLabel(master=self, text="Connection status: ", text_color=Colors.TEXT, text_font='Helvetica 11 bold', anchor=tkinter.W)
        self.connectionStatusText.grid(row=0, column=0, sticky=tkinter.NW, columnspan=2)

        self.connectionStatus = customtkinter.CTkLabel(master=self, text_font='Helvetica 11 bold')
        self.connectionStatus.grid(row=0, column=2, sticky=tkinter.NW, columnspan=2)
        self.SetConnectionStatus(False)

        def SetAvailableComPorts(comPorts):
            self.comPortOption.configure(values=comPorts)

        self.comPortOption = customtkinter.CTkOptionMenu(master=self, values=["Select port"], command=ComPortSelected, fg_color=Colors.BUTTON, button_color=Colors.BUTTON, button_hover_color=Colors.BUTTONHOVER, text_color=Colors.BUTTONTEXT)
        
        self.comPortOption.grid(row=1, column=0, sticky=tkinter.NW, columnspan=2)


        self.previewButton = customtkinter.CTkButton(master=self, text="↻",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: SetAvailableComPorts(Serial.GetPortNames()))
        self.previewButton.grid(row=1, column=2, sticky=tkinter.NW)

        self.connectButton = customtkinter.CTkButton(master=self, text="Connect",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=70, height=25, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.serial.Connect())
        self.connectButton.grid(row=2, column=0, sticky=tkinter.W)
        self.connectButton.grid_propagate(0)

        self.testConnectionButton = customtkinter.CTkButton(master=self, text="Test",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=70, height=25, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.serial.TestConnection())
        self.testConnectionButton.grid(row=2, column=1, sticky=tkinter.W)
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
        self.configure( width=300,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=2, column=0, padx=(0, 0), pady=(5, 0), sticky=tkinter.NW)
        self.grid_propagate(0)

        self.entry = customtkinter.CTkEntry(master=self, placeholder_text="MeriCode", width=120, height=25, border_width=2, corner_radius=10, text_color=Colors.BUTTONTEXT)
        self.entry.grid(row=0, column=0, sticky=tkinter.NW, columnspan=2)
        
        self.submitButton = customtkinter.CTkButton(master=self, text=">",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: SendEntryString())
        self.submitButton.grid(row=0, column=2, sticky=tkinter.NW)

        self.sendTestFile = customtkinter.CTkButton(master=self, text="Send File",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=100, height=28, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.serial.SendMeriCodeList())
        self.sendTestFile.grid(row=1, column=0, sticky=tkinter.NW, columnspan=1)

        def SendEntryString():
            self.parent.serial.WriteToSerial(self.entry.get())

class MeriCodeFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=300,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=3, column=0, padx=(0, 0), pady=(5, 0), sticky=tkinter.N)
        self.grid_propagate(0)

        self.submitButton = customtkinter.CTkButton(master=self, text="Generate MeriCode",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: self.GenerateMeriCode())
        self.submitButton.grid(row=0, column=2, sticky=tkinter.NW)

    def GenerateMeriCode(self):
        self.parent.canvas.canvas.CanvasToMeriCode()
        self.parent.serial.LoadMeriCodeFile()




class ToolSelect(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=480,
                        height=28,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=0, column=1, padx=(0, 0), pady=(5, 0), sticky=tkinter.NW)
        self.grid_propagate(0)

        self.lastDisabledButton = None

        self.penButton = customtkinter.CTkButton(master=self, text="Pen", fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.penButton.configure(command= lambda: self.SelectTool("Pen", self.penButton))
        self.penButton.grid(row=0, column=0, sticky=tkinter.W)

        self.moveButton = customtkinter.CTkButton(master=self, text="Move", fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT)
        self.moveButton.configure(command= lambda: self.SelectTool("Move", self.moveButton))
        self.moveButton.grid(row=0, column=1, sticky=tkinter.W)

        self.loadSVGButton = customtkinter.CTkButton(master=self, text="Load SVG", fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.LoadSVG())
        self.loadSVGButton.grid(row=0, column=2, sticky='e')

        self.SelectTool("Pen", self.penButton)

    def SelectTool(self, name, button):
        if button == self.lastDisabledButton:
            return
        if self.lastDisabledButton != None:
            self.lastDisabledButton.configure(state=tkinter.NORMAL)

        button.configure(state=tkinter.DISABLED)
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

        self.grid(row=1, column=1, padx=(0, 0), pady=(5, 0), sticky=tkinter.NW, rowspan=3)

        self.canvas = DrawingCanvas(self)
        self.canvas.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky=tkinter.NW)
        