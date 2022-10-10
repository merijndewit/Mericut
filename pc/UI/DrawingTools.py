from asyncio.windows_events import NULL
from mimetypes import init


import UI.DrawingShapes as DrawingShapes

class Tool():
    def __init__(self, parentCanvas):
        self.clicks = 0
        self.nodes = [None, None]
        self.parentCanvas = parentCanvas

class Node():
    def __init__(self, x, y):
        self.position = [x, y]
        self.connectedNodes = []
        

class Pen(Tool):
    def Clicked(self, x, y):
        if self.clicks == 0:
            self.nodes[0] = Node(x, y)
            self.clicks += 1
            return
        if self.clicks == 1:
            self.nodes[1] = Node(x, y)
            self.clicks = 0
            DrawingShapes.Line(self.nodes[0].position, self.nodes[1].position, self.parentCanvas)
            self.nodes = [None, None]
            return

