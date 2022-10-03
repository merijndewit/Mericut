import serial
import time
import customtkinter
import tkinter


#mericut
import TkinterRelated.Frames as Frames

from TkinterRelated.Colors import Colors


arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

#def write_read(x):
#    arduino.write(bytes(x, 'utf-8'))
#    time.sleep(0.05)
#    data = arduino.readline()
#    return data

#while True:
#    num = input("Enter a number: ")
#    value = write_read(num)
#    print(value)

class Main(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        self.geometry("800x480")
        self.configure(bg=Colors.BGCOLOR)
        self.title("Mericut")

        self.filamentViewFrame = Frames.ConnectFrame(self, self)

        self.mainloop();

if __name__ == "__main__":
    main = Main()