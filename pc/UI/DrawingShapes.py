from UI.Colors import Colors

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