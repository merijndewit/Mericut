from UI.Colors import Colors

class Shapes():
    def __init__(self, nodes, canvas):
        self.nodes = nodes
        self.canvas = canvas

class Line(Shapes):
    def __init__(self, nodes, canvas, draw = True):
        self.nodes = nodes
        self.canvas = canvas

        self.canvas.drawnShapes.append(self)

        if draw:
            self.Draw()

    def Draw(self):
        self.canvas.create_line(self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1], fill=Colors.GRIDCOLOR, width=3)
