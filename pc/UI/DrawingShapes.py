from UI.Colors import Colors
from UI.CanvasShapes import CanvasLine

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
        self.lines.append(CanvasLine(self.canvas, self.nodes[0].position[0] * self.canvas.canvasScale, self.nodes[0].position[1] * self.canvas.canvasScale, self.nodes[1].position[0] * self.canvas.canvasScale, self.nodes[1].position[1] * self.canvas.canvasScale, Colors.GRIDCOLOR, 3))

    def Update(self):
        self.lines[0].Move(self.nodes[0].position[0] * self.canvas.canvasScale, self.nodes[0].position[1] * self.canvas.canvasScale, self.nodes[1].position[0] * self.canvas.canvasScale, self.nodes[1].position[1] * self.canvas.canvasScale)

class QuadraticBezier(Shapes):
    def __init__(self, canvas, nodes, draw = True):
        self.canvas = canvas
        self.nodes = nodes
        self.lines = []
        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)
        
        if draw:
            self.Draw()

    def GetpointLocation(self, t):
        newNode = [0, 0]
        newNode[0] = math.pow(1 - t, 2) * self.nodes[0].position[0] + (1 - t) * 2 * t * self.nodes[1].position[0] + t * t * self.nodes[2].position[0]
        newNode[1] = math.pow(1 - t, 2) * self.nodes[0].position[1] + (1 - t) * 2 * t * self.nodes[1].position[1] + t * t * self.nodes[2].position[1]
        return newNode

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
        for i in range(20):
            if i == 0:
                startNode = self.GetpointLocation(i / 20)
                continue
            endNode = self.GetpointLocation(i / 20)
            if useOldLines:
                self.lines[i - 1].Move(int(startNode[0] * self.canvas.canvasScale), int(startNode[1] * self.canvas.canvasScale), int(endNode[0] * self.canvas.canvasScale), int(endNode[1] * self.canvas.canvasScale))
            else:
                self.lines.append(CanvasLine(self.canvas, int(startNode[0] * self.canvas.canvasScale), int(startNode[1] * self.canvas.canvasScale), int(endNode[0] * self.canvas.canvasScale), int(endNode[1] * self.canvas.canvasScale), Colors.GRIDCOLOR, 3))

            startNode = endNode

    def Update(self):
        self.Draw(True)