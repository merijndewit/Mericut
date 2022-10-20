from asyncio.windows_events import NULL
from mimetypes import init
from platform import node


import UI.DrawingShapes as DrawingShapes
import UI.CanvasUI as CanvasUI

import UI.Nodes as Nodes

class Tool():
    def __init__(self, parentCanvas):
        self.clicks = 0
        self.nodes = []
        self.parentCanvas = parentCanvas
        self.previewLines = []
        self.clickedNode = None

class Pen(Tool):
    def __init__(self, parentCanvas):
        super().__init__(parentCanvas)
        self.previewLine = None

    def Clicked(self, x, y, clickedNode):
        nodePositionX = x / self.parentCanvas.canvasScale
        nodePositionY = y / self.parentCanvas.canvasScale
        if clickedNode == None: #not clicked on any nodes
            self.nodes.append(Nodes.Node(nodePositionX, nodePositionY))
        elif (isinstance(clickedNode, Nodes.Node)): #clicked on a node
            self.nodes.append(Nodes.MergedNode(clickedNode.position, [Nodes.Node(x, y), clickedNode]))
        else: #clicked on a merged node
            clickedNode.AddNode(Nodes.Node(x, y))
            self.nodes.append(clickedNode)
        if self.clicks == 1:
            line = DrawingShapes.Line(self.nodes, self.parentCanvas)
            self.parentCanvas.drawnShapes.append(line) 
            for i in range(len(self.nodes)):
                self.nodes[i].AddShape(line)
            self.clicks = 0
            self.nodes = []
            self.parentCanvas.delete(self.previewLine.canvasLine)
            self.previewLine = None
            return

        self.clicks += 1

    def Hover(self, x, y):
        if self.clicks == 1:
            if self.previewLine == None:
                self.previewLine = CanvasUI.LineUI(self.nodes[0].position[0] * self.parentCanvas.canvasScale, self.nodes[0].position[1] * self.parentCanvas.canvasScale, x, y, self.parentCanvas)
                return
            self.previewLine.Move(self.nodes[0].position[0] * self.parentCanvas.canvasScale, self.nodes[0].position[1] * self.parentCanvas.canvasScale, x, y)
            return

class Move(Tool):
    def Clicked(self, x, y, clickedNode):
        self.clickedNode = clickedNode

    def Hover(self, x, y):
        nodePositionX = x / self.parentCanvas.canvasScale
        nodePositionY = y / self.parentCanvas.canvasScale
        if self.parentCanvas.mousePressed and self.clickedNode != None:
            self.clickedNode.position = [nodePositionX, nodePositionY]
            self.clickedNode.UpdateShape()
            return
        self.clickedNode = None



