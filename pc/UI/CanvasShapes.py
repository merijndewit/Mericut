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

    def Delete(self):
        self.canvas.delete(self.circle)

class CanvasLine():
    def __init__(self, canvas, x0, y0, x1, y1, color=Colors.GRIDCOLOR, width=1, dash=None):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 
        self.canvas = canvas
        self.color = color
        self.width = width
        self.dash = dash

        self.canvasLine = None
        self.Draw(self.canvas.canvasScale)

    def Draw(self, scale):
        self.canvasLine = self.canvas.create_line(int(self.x0 * scale), int(self.y0 * scale), int(self.x1 * scale), int(self.y1 * scale), fill=self.color, width=self.width, dash=self.dash)
    
    def Move(self, scale, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 
        self.canvas.coords(self.canvasLine, int(x0 * scale), int(y0 * scale), int(x1 * scale), int(y1 * scale))

    def Delete(self):
        self.canvas.delete(self.canvasLine)