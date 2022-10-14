from ast import Delete
import tkinter
import threading
import time
import math

from UI.Colors import Colors
import UI.CanvasTools as CanvasTools
import UI.DrawingTools as DrawingTools

class DrawingCanvas(tkinter.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure( width=590,
                        height=590,
                        highlightthickness=0,
                        bg=Colors.CANVASBACKGROUND)

        self.bind("<Button-1>", self.Clicked)
        self.bind('<ButtonRelease-1>',self.Released)
        self.bind('<Motion>', self.Motion)
        self.tool = DrawingTools.Pen(self)
        self.mousePosition = [0, 0]
        self.drawnShapes = []
        self.lastCollidedNode = None
        self.selectUIObject = None

        self.mousePressed = False

        CanvasTools.DrawGrid(self, 59)

    def SetTool(self, name):
        if name == "Pen":
            self.tool = DrawingTools.Pen(self)
            return
        if name == "Move":
            self.tool = DrawingTools.Move(self)
            return

    def Clicked(self, event):
        self.tool.Clicked(event.x, event.y, self.GetNearestNode(8))
        self.mousePressed = True

    def Released(self, event):
        self.mousePressed = False

    def Motion(self, event):
        x, y = event.x, event.y
        self.mousePosition = [x, y]
        self.tool.Hover(x, y)
        self.ShowColision ()

    def Redraw(self):
        self.delete("all")
        CanvasTools.DrawGrid(self, 59)
        for i in range(len(self.drawnShapes)):
            self.drawnShapes[i].Draw()

    def GetNearestNode(self, distance):
        nearestNode = None
        for i in range(len(self.drawnShapes)):
            for node in range(len(self.drawnShapes[i].nodes)):
                nodeDistance = abs(math.dist(self.drawnShapes[i].nodes[node].position, self.mousePosition))
                if nodeDistance > distance:
                    continue
                if nearestNode == None:
                    nearestNode = (i, node, nodeDistance)
                    continue
                if nearestNode[1] > nodeDistance:
                    nearestNode = (i, node, nodeDistance)
        if nearestNode == None:
            return None
        return self.drawnShapes[nearestNode[0]].nodes[nearestNode[node]]

    def ShowColision(self):
        collidingNode = self.GetNearestNode(8)
        if collidingNode == self.lastCollidedNode and collidingNode != None: #check if the mouse is still on the same node
            return
        if collidingNode == None:
            if self.selectUIObject == None:
                return
            self.selectUIObject.Move(-20, -20)
            return
        if self.selectUIObject == None:
            self.selectUIObject = CanvasTools.CircleUI(collidingNode.position[0], collidingNode.position[1], 8, self)
            return
        self.selectUIObject.Move(collidingNode.position[0], collidingNode.position[1])