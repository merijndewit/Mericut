from UI.Colors import Colors
#from UI.ProgramFrames.CanvasFrame import Canvas

class CanvasShapes():
    def __init__(self):
        pass

class CanvasCircle(CanvasShapes):
    def __init__(self, x, y, radius, canvas, color):
        self.x = x
        self.y = y 
        self.radius = radius
        self.canvas = canvas
        self.circle = None
        self.canvasFrame = canvas.parent
        self.color = color
        self.Draw()

    def Draw(self):
        pass
        #self.circle = self.canvasFrame.DrawCircle(self.x, self.y, self.radius, self.color)
    
    def Move(self, x, y):
        self.x = x
        self.y = y 
        self.Draw()

    def SetScale(self, scale):
        pass
        #self.canvas.coords(self.circle, int(self.x * scale) - self.radius, int(self.y * scale) - self.radius, int(self.x * scale) + self.radius, int(self.y * scale) + self.radius)

    def Delete(self):
        self.canvas.delete(self.circle)

class CanvasLine(CanvasShapes):
    def __init__(self, canvasFrame, x0, y0, x1, y1, color=Colors.GRIDCOLOR, width=1):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 
        self.canvasFrame = canvasFrame
        self.color = color
        self.width = width

        self.canvasLine = None
        self.Draw()

    def Draw(self):
        self.canvasLine = self.canvasFrame.DrawLine(self.x0, self.y0, self.x1, self.y1, self.color)
        
    def Move(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 
        self.Draw()

    def Delete(self):
        pass
        #self.canvas.delete(self.canvasLine)

    def Update(self):
        self.Draw()
        #self.canvas.coords(self.canvasLine, (self.x0 * self.canvas.canvasScale) + self.canvas.screenOffsetX, (self.y0 * self.canvas.canvasScale) + self.canvas.screenOffsetY, (self.x1 * self.canvas.canvasScale) + self.canvas.screenOffsetX, (self.y1 * self.canvas.canvasScale) + self.canvas.screenOffsetY)
