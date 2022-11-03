from UI.Colors import Colors
from UI.CanvasShapes import CanvasLine
import VectorMath

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

class QuadraticBezier(Shapes):
    def __init__(self, canvas, nodes, draw = True):
        self.canvas = canvas
        self.nodes = nodes
        self.lines = []
        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)
        
        if draw:
            self.Draw()

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
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

    def Update(self):
        self.Draw(True)