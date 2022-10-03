import serial
import time
import customtkinter
import tkinter

#mericut
import TkinterRelated.Frames as Frames
from Serial import Serial

from TkinterRelated.Colors import Colors
from Serial import Serial


arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

class Main(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        self.geometry("800x480")
        self.configure(bg=Colors.BGCOLOR)
        self.title("Mericut")

        self.serial = Serial()

        self.filamentViewFrame = Frames.ConnectFrame(self, self)

        self.mainloop();

if __name__ == "__main__":
    main = Main()