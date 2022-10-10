from UI.Colors import Colors

class Line():
    def __init__(self, node0, node1, canvas, draw = True):
        self.node0 = node0
        self.node1 = node1
        self.canvas = canvas

        if draw:
            self.DrawLine()

    def DrawLine(self):
        self.canvas.create_line(self.node0[0], self.node0[1], self.node1[0], self.node1[1], fill=Colors.GRIDCOLOR, width=1)