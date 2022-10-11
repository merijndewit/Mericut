from asyncio.windows_events import NULL
from mimetypes import init


import UI.DrawingShapes as DrawingShapes
import UI.CanvasTools as CanvasTools

class Tool():
    def __init__(self, parentCanvas):
        self.clicks = 0
        self.nodes = []
        self.parentCanvas = parentCanvas
        self.previewLines = []

class Node():
    def __init__(self, x, y):
        self.position = [x, y]
        self.connectedNodes = []

class Pen(Tool):
    def Clicked(self, x, y):
        self.nodes.append(Node(x, y))
        
        if self.clicks == 1:
            DrawingShapes.Line(self.nodes, self.parentCanvas)
            self.clicks = 0
            self.nodes = []
            return

        self.clicks += 1

    def Hover(self, x, y):
        for i in range(len(self.previewLines)):
            self.parentCanvas.delete(self.previewLines[i])
        if self.clicks == 1:
            previewLine = CanvasTools.DrawLine(self.parentCanvas, self.nodes[0].position[0], self.nodes[0].position[1], x, y)
            self.previewLines.append(previewLine)



