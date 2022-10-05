from cgitb import text
import customtkinter
import tkinter

from TkinterRelated.Colors import Colors
from Serial import Serial

class ConnectFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=300,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGFRAME)

        self.grid(row=0, column=0, padx=(0, 0), pady=(5, 0), sticky=tkinter.NE)
        self.grid_propagate(0)

        def ComPortSelected(choice):
            self.parent.serial.selectedComPort = choice




        self.connectionStatusText = customtkinter.CTkLabel(master=self, text="Connection status: ", text_color="#ffffff", text_font='Helvetica 11 bold', anchor=tkinter.W)
        self.connectionStatusText.grid(row=0, column=0, sticky=tkinter.NW, columnspan=2)

        self.connectionStatus = customtkinter.CTkLabel(master=self, text_font='Helvetica 11 bold')
        self.connectionStatus.grid(row=0, column=2, sticky=tkinter.NW, columnspan=2)
        self.SetConnectionStatus(False)

        def SetAvailableComPorts(comPorts):
            self.comPortOption.configure(values=comPorts)

        self.comPortOption = customtkinter.CTkOptionMenu(master=self, values=[], command=ComPortSelected, fg_color=Colors.BUTTON, button_color=Colors.BUTTON, button_hover_color=Colors.BUTTONHOVER)
        
        self.comPortOption.grid(row=1, column=0, sticky=tkinter.NW, columnspan=2)


        self.previewButton = customtkinter.CTkButton(master=self, text="↻",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=28, height=28, command= lambda: SetAvailableComPorts(Serial.GetPortNames()))
        self.previewButton.grid(row=1, column=2, sticky=tkinter.NW)

        self.connectButton = customtkinter.CTkButton(master=self, text="Connect",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=70, height=25, command= lambda: self.parent.serial.Connect())
        self.connectButton.grid(row=2, column=0, sticky=tkinter.W)
        self.connectButton.grid_propagate(0)

        self.testConnectionButton = customtkinter.CTkButton(master=self, text="Test",  fg_color=Colors.BUTTON, hover_color=Colors.BUTTONHOVER, text_font=("", 11), width=70, height=25, command= lambda: self.parent.serial.TestConnection())
        self.testConnectionButton.grid(row=2, column=1, sticky=tkinter.W)
        self.testConnectionButton.grid_propagate(0)

    def SetConnectionStatus(self, bool):
        if bool:
            self.connectionStatus.configure(text="Connected!", text_color=Colors.CONNECTEDTEXT)
            return
        self.connectionStatus.configure(text="Disconnected.", text_color=Colors.DISCONNECTEDTEXT)
        
