from UI.Colors import Colors

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
        self.canvasLine = None

        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)

        if draw:
            self.Draw()

    def Draw(self):
        self.canvasLine = self.canvas.create_line(self.nodes[0].position[0] * self.canvas.canvasScale, self.nodes[0].position[1] * self.canvas.canvasScale, self.nodes[1].position[0] * self.canvas.canvasScale, self.nodes[1].position[1] * self.canvas.canvasScale, fill=Colors.GRIDCOLOR, width=3)

    def Update(self):
        self.canvas.coords(self.canvasLine, self.nodes[0].position[0] * self.canvas.canvasScale, self.nodes[0].position[1] * self.canvas.canvasScale, self.nodes[1].position[0] * self.canvas.canvasScale, self.nodes[1].position[1] * self.canvas.canvasScale)

class QuadraticBezier(Shapes):
    def __init__(self, canvas, node0, node1, node2, draw = True):
        self.canvas = canvas
        self.nodes = [node0, node1, node2]
        self.lines = []
        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)
        
        if draw:
            self.Draw()

    def RecalculatePoints(self, t):
        newNode = [0, 0]
        newNode[0] = int(math.pow(1 - t, 2) * self.nodes[0].position[0] + (1 - t) * 2 * t * self.nodes[1].position[0] + t * t * self.nodes[2].position[0])
        newNode[1] = int(math.pow(1 - t, 2) * self.nodes[0].position[1] + (1 - t) * 2 * t * self.nodes[1].position[1] + t * t * self.nodes[2].position[1])
        return newNode

    def Draw(self):
        startNode = [0, 0]
        endNode = [0, 0]
        for i in range(20):
            if i == 0:
                startNode = self.RecalculatePoints(i / 20)
                continue
            endNode = self.RecalculatePoints(i / 20)

            self.lines.append(self.canvas.create_line(startNode[0] * self.canvas.canvasScale, startNode[1] * self.canvas.canvasScale, endNode[0] * self.canvas.canvasScale, endNode[1] * self.canvas.canvasScale, fill=Colors.GRIDCOLOR, width=3))

            startNode = endNode
            print(startNode, endNode)

    def Update(self):
        self.canvas.coords(self.canvasLine, self.nodes[0].position[0] * self.canvas.canvasScale, self.nodes[0].position[1] * self.canvas.canvasScale, self.nodes[1].position[0] * self.canvas.canvasScale, self.nodes[1].position[1] * self.canvas.canvasScale)