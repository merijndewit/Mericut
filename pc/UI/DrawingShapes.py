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

    def Draw(self):
        self.lines.append(CanvasLine(self.canvas, self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1], Colors.GRIDCOLOR, 3))

    def Update(self):
        self.lines[0].Move(self.canvas.canvasScale, self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1])

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
        for i in range(21):
            if i == 0:
                startNode = VectorMath.QuadraticBezier(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, i / 20)
                continue
            endNode = VectorMath.QuadraticBezier(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, i / 20)
            if useOldLines:
                self.lines[i - 1].Move(self.canvas.canvasScale, startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.GRIDCOLOR, 3))

            startNode = endNode

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.canvas.canvasScale, self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1])
            self.helpLines[1].Move(self.canvas.canvasScale, self.nodes[2].position[0], self.nodes[2].position[1], self.nodes[1].position[0], self.nodes[1].position[1])
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1], Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].position[0], self.nodes[2].position[1], self.nodes[1].position[0], self.nodes[1].position[1], Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)

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
        for i in range(21):
            if i == 0:
                startNode = VectorMath.CubicBezier(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, self.nodes[3].position, i / 20)
                continue
            endNode = VectorMath.CubicBezier(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, self.nodes[3].position, i / 20)
            if useOldLines:
                self.lines[i - 1].Move(self.canvas.canvasScale, startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.GRIDCOLOR, 3))

            startNode = endNode

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.canvas.canvasScale, self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1])
            self.helpLines[1].Move(self.canvas.canvasScale, self.nodes[2].position[0], self.nodes[2].position[1], self.nodes[3].position[0], self.nodes[3].position[1])
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1], Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].position[0], self.nodes[2].position[1], self.nodes[3].position[0], self.nodes[3].position[1], Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)

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
        x0 = self.nodes[0].position[0]
        y0 = self.nodes[0].position[1]
        x1 = self.nodes[2].position[0]
        y1 = self.nodes[2].position[1]
        x2 = self.nodes[1].position[0]
        y2 = self.nodes[1].position[1]

        r = math.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))
        x = x0-r
        y = y0-r
        width = 2*r
        height = 2*r
        startAngle = (math.degrees(math.atan2(y0-y2, x0-x2)))
        endAngle = (math.degrees(math.atan2(y1-y2, x1-x2)))
        if (startAngle < 0):
            startAngle = 180 + (180 - abs(startAngle))

        if (endAngle < 0):
            endAngle = 180 + (180 - abs(endAngle))

        angle = endAngle + abs((startAngle * t) - abs(endAngle * t))
        print(startAngle , endAngle, abs(startAngle - endAngle))

        xP = x2 + r * math.cos(angle * math.pi / 180)
        yP = y2 + r * math.sin(angle * math.pi / 180)

        return [xP, yP]

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
        self.DrawHelpLines(useOldLines)
        for i in range(21):
            if i == 0:
                startNode = self.GetArcPoint(i / 20)
                continue
            endNode = self.GetArcPoint(i / 20)
            if useOldLines:
                self.lines[i - 1].Move(self.canvas.canvasScale, startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.GRIDCOLOR, 3))

            startNode = endNode

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.canvas.canvasScale, self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1])
            self.helpLines[1].Move(self.canvas.canvasScale, self.nodes[2].position[0], self.nodes[2].position[1], self.nodes[1].position[0], self.nodes[1].position[1])
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1], Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].position[0], self.nodes[2].position[1], self.nodes[1].position[0], self.nodes[1].position[1], Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)