import customtkinter
import tkinter

from UI.Colors import Colors

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

        self.deletebutton = customtkinter.CTkButton(master=self, text="x", fg_color=Colors.BUTTON, hover_color=Colors.PAPERHOVERCOLOR, width=12, height=12, text_color=Colors.BUTTONTEXT, command= lambda: self.DeleteLayer())
        self.deletebutton.grid(row=3, column=1, padx=(0, 0), pady=(0, 0), sticky=tkinter.SW)

    def SelectLayer(self):
        self.parent.parent.hardwareAcceleratedCanvas.canvas.SelectLayer(self.name)

    def TransformLayer(self):
        self.parent.parent.hardwareAcceleratedCanvas.canvas.TransformLayer(self.name)

    def DeleteLayer(self):
        self.parent.parent.hardwareAcceleratedCanvas.canvas.DeleteLayer(self.name)
        self.destroy()


class CanvasLayerFrame(customtkinter.CTkFrame):
    def __init__(self, parent, frameParent, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=200,
                        height=120,
                        corner_radius=4,
                        fg_color=Colors.BGCOLOR)

        self.grid(row=3, column=2, padx=(5, 5), pady=(5, 5), rowspan=1, sticky=tkinter.NSEW)
        self.grid_propagate(False)
        self.maxWidth = 3
        
        self.row :int = 0

        self.header = customtkinter.CTkLabel(master=self, text="Layers", text_color=Colors.TEXT, font=("Arial Bold", 11), anchor=tkinter.W)
        self.header.grid(row=self.row, column=0, sticky=tkinter.S, columnspan=4)

        ##### next row
        self.row += 1

        self.label = customtkinter.CTkLabel(master=self, text="", fg_color=Colors.SEPERATIONLINE, height=2)
        self.label.grid(row=self.row, column=0, sticky=tkinter.EW, columnspan=4, pady=(5, 5), padx=(5, 5))
        self.label.grid_propagate(False)

        ##### next row
        self.row += 1
        
        self.moveButton = customtkinter.CTkButton(master=self, text="Add new layer", fg_color=Colors.PAPERBACKGROUND, hover_color=Colors.PAPERHOVERCOLOR, font=("", 11), width=40, height=40, text_color=Colors.BUTTONTEXT, command= lambda: self.parent.canvas.canvas.AddLayer())
        self.moveButton.grid(row=self.row, column=0, pady=(0, 5), sticky=tkinter.NW)

        ##### next row
        self.row += 1

        layerNames = self.parent.hardwareAcceleratedCanvas.canvas.GetLayerNames()
        self.layerFrames = []
        for i in range(len(layerNames)):
            self.AddLayerButton(layerNames[i])

            
    def AddLayerButton(self, name):
        posX = len(self.layerFrames) % 3
        posY = int(len(self.layerFrames) / 3) + self.row
        if posX == self.maxWidth:
            posX = 0
            posY += 1

        layerFrame = LayerButtonFrame(self, self, name)
        layerFrame.grid(row=posY, column=posX, sticky=tkinter.NW)
        layerFrame.grid_propagate(False)
        self.layerFrames.append(layerFrame)