from UI.Colors import Colors
from UI.CanvasShapes import CanvasLine
import VectorMath
import math

class Shapes():
    def __init__(self, nodes, canvas):
        self.nodes = nodes
        self.canvas = canvas

    def ReplaceNode(self, nodeToReplace, newNode):
        for i in range(len(self.nodes)):
            if (self.nodes[i] == nodeToReplace):
                self.nodes[i] = newNode

class Line(Shapes):
    def __init__(self, nodes, canvas, draw = True):
        self.nodes = nodes
        self.canvas = canvas
        self.lines = []

        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)

        if draw:
            self.Draw()

    def Scale(self, scale):
        self.layerScale = scale
        self.Update()

    def Draw(self):
        self.lines.append(CanvasLine(self.canvas, self.nodes[0].GetPositionX(), self.nodes[0].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY(), Colors.GRIDCOLOR, 3))

    def Update(self):
        self.lines[0].Move(self.canvas.canvasScale, self.nodes[0].GetPositionX(), self.nodes[0].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY())

    def GetStartPosition(self):
        return self.nodes[0].GetPosition()

    def GetEndPosition(self):
        return self.nodes[1].GetPosition()

class QuadraticBezier(Shapes): #takes 3 nodes [start, control, end]
    def __init__(self, canvas, nodes, draw = True):
        self.canvas = canvas
        self.nodes = nodes
        self.lines = []
        self.helpLines = []
        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)
        
        if draw:
            self.Draw()

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
        self.DrawHelpLines(useOldLines)
        resolution = int(math.dist(self.nodes[0].GetPosition(), self.nodes[2].GetPosition()) / 3) + 1
        for i in range(resolution + 1):
            if i == 0:
                startNode = VectorMath.QuadraticBezier(self.nodes[0].GetPosition(), self.nodes[1].GetPosition(), self.nodes[2].GetPosition(), i / resolution)
                continue
            endNode = VectorMath.QuadraticBezier(self.nodes[0].GetPosition(), self.nodes[1].GetPosition(), self.nodes[2].GetPosition(), i / resolution)
            if useOldLines and len(self.lines) >= resolution:
                self.lines[i - 1].Move(self.canvas.canvasScale, startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.GRIDCOLOR, 3))

            startNode = endNode

        if len(self.lines) > resolution:
            toDelete = len(self.lines) - resolution
            for i in range(resolution, len(self.lines)):
                self.lines[i].Delete()
            del self.lines[len(self.lines) - toDelete:]

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.canvas.canvasScale, self.nodes[0].GetPositionX(), self.nodes[0].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY())
            self.helpLines[1].Move(self.canvas.canvasScale, self.nodes[2].GetPositionX(), self.nodes[2].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY())
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].GetPositionX(), self.nodes[0].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY(), Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].GetPositionX(), self.nodes[2].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY(), Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)

    def GetStartPosition(self):
        return self.nodes[0].GetPosition()

    def GetEndPosition(self):
        return self.nodes[2].GetPosition()

class CubicBezier(Shapes): #takes 4 nodes [start, control0, control1, end]
    def __init__(self, canvas, nodes, draw = True):
        self.canvas = canvas
        self.nodes = nodes
        self.lines = []
        self.helpLines = []
        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)
        
        if draw:
            self.Draw()

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
        self.DrawHelpLines(useOldLines)
        resolution = int(math.dist(self.nodes[0].GetPosition(), self.nodes[3].GetPosition()) / 3) + 1
        for i in range(resolution + 1):
            if i == 0:
                startNode = VectorMath.CubicBezier(self.nodes[0].GetPosition(), self.nodes[1].GetPosition(), self.nodes[2].GetPosition(), self.nodes[3].GetPosition(), i / resolution)
                continue
            endNode = VectorMath.CubicBezier(self.nodes[0].GetPosition(), self.nodes[1].GetPosition(), self.nodes[2].GetPosition(), self.nodes[3].GetPosition(), i / resolution)
            if useOldLines and len(self.lines) >= resolution:
                self.lines[i - 1].Move(self.canvas.canvasScale, startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.GRIDCOLOR, 3))

            startNode = endNode

        if len(self.lines) > resolution:
            toDelete = len(self.lines) - resolution
            for i in range(resolution, len(self.lines)):
                self.lines[i].Delete()
            del self.lines[len(self.lines) - toDelete:]

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.canvas.canvasScale, self.nodes[0].GetPositionX(), self.nodes[0].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY())
            self.helpLines[1].Move(self.canvas.canvasScale, self.nodes[2].GetPositionX(), self.nodes[2].GetPositionY(), self.nodes[3].GetPositionX(), self.nodes[3].GetPositionY())
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].GetPositionX(), self.nodes[0].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY(), Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].GetPositionX(), self.nodes[2].GetPositionY(), self.nodes[3].GetPositionX(), self.nodes[3].GetPositionY(), Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)

    def GetStartPosition(self):
        return self.nodes[0].GetPosition()

    def GetEndPosition(self):
        return self.nodes[3].GetPosition()

class Arc(Shapes): #takes 3 nodes [start, control, end]
    def __init__(self, canvas, nodes, draw = True):
        self.canvas = canvas
        self.nodes = nodes
        self.lines = []
        self.helpLines = []
        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)
        
        if draw:
            self.Draw()

    def GetArcPoint(self, t):
        x0 = self.nodes[0].GetPositionX()
        y0 = self.nodes[0].GetPositionY()
        x1 = self.nodes[2].GetPositionX()
        y1 = self.nodes[2].GetPositionY()
        x2 = self.nodes[1].GetPositionX()
        y2 = self.nodes[1].GetPositionY()

        r = math.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))
        x = x0-r
        y = y0-r
        width = 2*r
        height = 2*r
        startAngle = (math.degrees(math.atan2(y0-y2, x0-x2)))
        endAngle = (math.degrees(math.atan2(y1-y2, x1-x2)))
        angle = endAngle + ((startAngle * t) - (endAngle * t))

        if startAngle < 0:
            startAngle += 180
        if endAngle < 0:
            endAngle += 180
    
        xP = x2 + r * math.cos(angle * math.pi / 180)
        yP = y2 + r * math.sin(angle * math.pi / 180)


        normalizedEndAngle = 0
        FullCircleAngle = 2 * math.pi
        if (startAngle < endAngle):
            normalizedEndAngle = endAngle
        
        else:
            normalizedEndAngle = endAngle + FullCircleAngle

        angleRange = normalizedEndAngle - startAngle
        if angleRange > FullCircleAngle:
            angleRange = FullCircleAngle
        else:
            angleRange = angleRange

        step = angleRange / 20
        currentAngle = startAngle

        points = []
        while (currentAngle <= normalizedEndAngle):
            x = x2 + r * math.cos(currentAngle)
            y = y2 + r * math.sin(currentAngle)
            points.append([x, y])
            currentAngle += step

        return points

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
        self.DrawHelpLines(useOldLines)
        points = self.GetArcPoint(0.1)
        for i in range(20):
            if i == 0:
                startNode = points[0]
                continue
            endNode = points[i]
            if useOldLines:
                self.lines[i - 1].Move(self.canvas.canvasScale, startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.GRIDCOLOR, 3))

            startNode = endNode

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.canvas.canvasScale, self.nodes[0].GetPositionX(), self.nodes[0].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY())
            self.helpLines[1].Move(self.canvas.canvasScale, self.nodes[2].GetPositionX(), self.nodes[2].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY())
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].GetPositionX(), self.nodes[0].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY(), Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].GetPositionX(), self.nodes[2].GetPositionY(), self.nodes[1].GetPositionX(), self.nodes[1].GetPositionY(), Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)