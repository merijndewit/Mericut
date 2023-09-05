from UI.Colors import Colors
#from UI.ProgramFrames.CanvasFrame import Canvas

class CanvasShapes():
    def __init__(self):
        pass

class CanvasCircle(CanvasShapes):
    def __init__(self, x, y, radius, canvas):
        self.x = x
        self.y = y 
        self.radius = radius
        self.canvas = canvas
        self.circle = None
        self.Draw()

    def Draw(self):
        pass
        #self.circle = self.canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, outline=Colors.COLISIONNODE, width=2)
    
    def SetScale(self, scale):
        pass
        #self.canvas.coords(self.circle, int(self.x * scale) - self.radius, int(self.y * scale) - self.radius, int(self.x * scale) + self.radius, int(self.y * scale) + self.radius)

    def Move(self, x, y):
        pass
        #self.canvas.coords(self.circle, x - self.radius, y - self.radius, x + self.radius, y + self.radius)
        self.x = x
        self.y = y
        
    def SetColor(self, color):
        self.canvas.itemconfig(self.circle, outline=color)

    def Delete(self):
        self.canvas.delete(self.circle)

class CanvasRectangle(CanvasShapes):
    def __init__(self, position :list, width, height, canvas, tags=""):
        self.width = width
        self.height = height
        self.x = position[0]
        self.y = position[1]
        self.canvas = canvas
        self.rectangle = None
        self.tag = tags
        self.Draw()

    def Draw(self):
        pass
        #self.rectangle = self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=Colors.COLISIONNODE, tags=(self.tag), width=0)
    
    def Update(self, position, scale):
        self.x = position[0]
        self.y = position[1]
        #self.canvas.coords(self.rectangle, int(self.x), int(self.y), int((self.width * scale) + self.x), int((self.height * scale) + self.y))

    def Move(self, x, y):
        pass
        #self.canvas.coords(self.rectangle, x, y, x + self.width, y + self.height)

    def SetColor(self, color):
        pass
        #self.canvas.itemconfig(self.rectangle, fill=color)

    def Delete(self):
        pass
        #self.canvas.delete(self.rectangle)

class CanvasLine(CanvasShapes):
    def __init__(self, canvas, x0, y0, x1, y1, color=Colors.GRIDCOLOR, width=1, dash=None, scaleWithCanvas=False):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 
        self.canvas = canvas
        self.color = color
        self.width = width
        self.dash = dash
        self.scaleWithCanvas = scaleWithCanvas
        self.canvasFrame = canvas.parent

        self.canvasLine = None
        self.Draw()

    def Draw(self):
        if self.scaleWithCanvas:
            self.canvasLine = self.canvasFrame.DrawLine((self.x0 * self.canvas.canvasScale) + self.canvas.screenOffsetX, (self.y0 * self.canvas.canvasScale) + self.canvas.screenOffsetY, (self.x1 * self.canvas.canvasScale) + self.canvas.screenOffsetX, (self.y1 * self.canvas.canvasScale) + self.canvas.screenOffsetY)
            return
        self.canvasLine = self.canvasFrame.DrawLine(self.x0, self.y0, self.x1, self.y1)
        
    def Move(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0 
        self.x1 = x1
        self.y1 = y1 
        if self.scaleWithCanvas:
            self.canvas.coords(self.canvasLine, (self.x0 * self.canvas.canvasScale) + self.canvas.screenOffsetX, (self.y0 * self.canvas.canvasScale) + self.canvas.screenOffsetY, (self.x1 * self.canvas.canvasScale) + self.canvas.screenOffsetX, (self.y1 * self.canvas.canvasScale) + self.canvas.screenOffsetY)
            return
        self.canvas.coords(self.canvasLine, x0, y0, x1, y1)

    def Delete(self):
        self.canvas.delete(self.canvasLine)

    def Update(self):
        self.canvas.coords(self.canvasLine, (self.x0 * self.canvas.canvasScale) + self.canvas.screenOffsetX, (self.y0 * self.canvas.canvasScale) + self.canvas.screenOffsetY, (self.x1 * self.canvas.canvasScale) + self.canvas.screenOffsetX, (self.y1 * self.canvas.canvasScale) + self.canvas.screenOffsetY)
