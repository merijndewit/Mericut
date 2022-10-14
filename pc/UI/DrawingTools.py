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
        self.clickedNode = None

class Node():
    def __init__(self, x, y):
        self.position = [x, y]
        self.connectedNodes = []
        self.shape = None

class Pen(Tool):
    def Clicked(self, x, y, clickedNode):
        if clickedNode != None:
            self.nodes.append(clickedNode)
        else:
            self.nodes.append(Node(x, y))
        
        if self.clicks == 1:
            self.parentCanvas.drawnShapes.append(DrawingShapes.Line(self.nodes, self.parentCanvas)) 
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

class Move(Tool):
    def Clicked(self, x, y, clickedNode):
        self.clickedNode = clickedNode

    def Hover(self, x, y):
        if self.parentCanvas.mousePressed and self.clickedNode != None:
            self.clickedNode.position = [x, y]
            self.clickedNode.shape.Update()
            return
        self.clickedNode = None



