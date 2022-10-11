from ast import Delete
import tkinter
import threading
import time
import math

from UI.Colors import Colors
import UI.CanvasTools as CanvasTools
import UI.DrawingTools as DrawingTools

class DrawingCanvas(tkinter.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure( width=590,
                        height=590,
                        highlightthickness=0,
                        bg=Colors.CANVASBACKGROUND)

        self.bind("<Button-1>", self.Clicked)
        self.bind('<Motion>', self.Motion)
        self.tool = DrawingTools.Pen(self)
        self.mousePosition = [0, 0]
        self.drawnShapes = []
        self.drawnUI = []


        CanvasTools.DrawGrid(self, 59)

        self.colisionThread = threading.Thread(target=self.CheckColision, daemon=True)
        self.colisionThread.start()
        

    def Clicked(self, event):
        self.tool.Clicked(event.x, event.y)

    def Motion(self, event):
        x, y = event.x, event.y
        self.mousePosition = [x, y]

    def Redraw(self):
        self.delete("all")
        CanvasTools.DrawGrid(self, 59)
        for i in range(len(self.drawnShapes)):
            self.drawnShapes[i].Draw()
        

    def CheckColision(self):
        while True:
            time.sleep(0.020)
            for i in range(len(self.drawnUI)):
                self.delete(self.drawnUI[i])
            self.drawnUI = []
            for i in range(len(self.drawnShapes)):
                for node in range(len(self.drawnShapes[i].nodes)):
                    distance = abs(math.dist(self.drawnShapes[i].nodes[node].position, self.mousePosition))
                    if distance < 8:
                        newCircle = CanvasTools.DrawCircle(self, self.drawnShapes[i].nodes[node].position[0], self.drawnShapes[i].nodes[node].position[1], 8)
                        self.drawnUI.append(newCircle)