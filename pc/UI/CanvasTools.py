from re import X
from tkinter import Y
from UI.Colors import Colors

def DrawGrid(canvas, cellSize, edges = False):
    for i in range(int(canvas.winfo_reqwidth() / cellSize)):
        if not i or i is int(canvas.winfo_reqwidth() / cellSize) and not edges: continue
        canvas.create_line((i * cellSize), 0, (i * cellSize), canvas.winfo_reqheight(), fill=Colors.GRIDCOLOR, width=1)
    for i in range(int(canvas.winfo_reqheight() / cellSize)):
        if not i or i is int(canvas.winfo_reqheight() / cellSize) and not edges: continue
        canvas.create_line(0, (i * cellSize), canvas.winfo_reqwidth(), (i * cellSize), fill=Colors.GRIDCOLOR, width=1)
    return canvas

class CircleUI():
    def __init__(self, x, y, radius, canvas):
        self.x = x
        self.y = y 
        self.radius = radius
        self.canvas = canvas
        self.circle = None
        self.DrawCircle()

    def DrawCircle(self):
        self.circle = self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, outline=Colors.COLISIONCIRCLECOLOR, width=2)
    
    def Move(self, x, y):
        self.canvas.coords(self.circle, x - self.radius, y - self.radius, x + self.radius, y + self.radius)

class LineUI():
    def __init__(self, x, y, x1, y1, canvas):
        self.x = x
        self.y = y 
        self.x1 = x1
        self.y1 = y1 
        self.canvas = canvas
        self.canvasLine = None
        self.DrawLine()

    def DrawLine(self):
        self.canvasLine = self.canvas.create_line(self.x, self.y, self.x1, self.y1, fill=Colors.GRIDCOLOR, width=1)
    
    def Move(self, x, y, x1, y1):
        self.canvas.coords(self.canvasLine, x, y, x1, y1)

