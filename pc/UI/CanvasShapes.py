from UI.Colors import Colors

class CanvasCircle():
    def __init__(self, x, y, radius, canvas):
        self.x = x
        self.y = y 
        self.radius = radius
        self.canvas = canvas
        self.circle = None
        self.Draw()

    def Draw(self):
        self.circle = self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, outline=Colors.COLISIONNODE, width=2)
    
    def Move(self, x, y):
        self.canvas.coords(self.circle, x - self.radius, y - self.radius, x + self.radius, y + self.radius)

    def SetColor(self, color):
        self.canvas.itemconfig(self.circle, outline=color)

class CanvasLine():
    def __init__(self, x, y, x1, y1, canvas):
        self.x = x
        self.y = y 
        self.x1 = x1
        self.y1 = y1 
        self.canvas = canvas
        self.canvasLine = None
        self.Draw()

    def Draw(self):
        self.canvasLine = self.canvas.create_line(self.x, self.y, self.x1, self.y1, fill=Colors.GRIDCOLOR, width=1)
    
    def Move(self, x, y, x1, y1):
        self.canvas.coords(self.canvasLine, x, y, x1, y1)