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
    def __init__(self, canvas, x0, y0, x1, y1, color=Colors.GRIDCOLOR, width=1):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 
        self.canvas = canvas
        self.color = color
        self.width = width

        self.canvasLine = None
        self.Draw()

    def Draw(self):
        self.canvasLine = self.canvas.create_line(self.x0, self.y0, self.x1, self.y1, fill=self.color, width=self.width)
    
    def Move(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 
        self.canvas.coords(self.canvasLine, x0, y0, x1, y1)