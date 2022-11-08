import tkinter
import math

from UI.Colors import Colors
import UI.CanvasUI as CanvasUI
import UI.CanvasShapes as CanvasShapes
import UI.DrawingTools as DrawingTools
import UI.CanvasSVG as CanvasSVG
import UI.CanvasToMeriCode as CanvasToMeriCode

class DrawingCanvas(tkinter.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tkinter.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure( width=590,
                        height=590,
                        highlightthickness=0,
                        bg=Colors.CANVASBACKGROUND)

        self.bind("<Button-1>", self.Clicked)
        self.bind('<MouseWheel>', self.Scroll)
        self.bind('<ButtonRelease-1>',self.Released)
        self.bind('<Motion>', self.Motion)
        self.bind("<Configure>", self.ResizedWindow)

        self.tool = DrawingTools.Pen(self)
        self.mousePosition = [0, 0]
        self.drawnShapes = []
        self.lastCollidedNode = None
        self.background = None

        self.pixelsPerMM = 10
        self.canvasScale = 1

        self.mousePressed = False
        self.snap = True

        self.canvasGrid = CanvasUI.CanvasGrid(self, self.pixelsPerMM)
        self.selectUIObject = CanvasShapes.CanvasCircle(-20, -20, 8, self)

    def ResizedWindow(self,event):
        width = event.width
        height = event.height

        self.config(width=width, height=height)
        if self.background is not None:
            self.background.SetScale(self.canvasScale)
        self.RedrawGrid()
        self.RedrawShapes()

        #self.scale("all",0,0,wscale,hscale)

    def SetBackground(self, background = "", customSize = None):
        width = 0
        height = 0
        color = "#000000"
        if customSize is not None:
            width = customSize[0]
            height = customSize[1]
            color = Colors.PAPERBACKGROUNDCANVAS
        elif background == "A4":
            width = 210
            height = 297
            color = Colors.PAPERBACKGROUNDCANVAS
        elif background == "A5":
            width = 148.5
            height = 210
            color = Colors.PAPERBACKGROUNDCANVAS
        elif background == "A6":
            width = 105
            height = 148.5
            color = Colors.PAPERBACKGROUNDCANVAS
        self.background = CanvasShapes.CanvasRectangle(width, height, self)
        self.background.SetColor(color)
        

    def Scroll(self, event):
        self.pixelsPerMM += (-1*(event.delta/120)) * 2
        self.canvasScale = self.pixelsPerMM / 10
        if self.pixelsPerMM <= 0:
            self.pixelsPerMM = 2
            self.canvasScale = self.pixelsPerMM / 10
        if self.background is not None:
            self.background.SetScale(self.canvasScale)
        self.RedrawGrid()
        self.RedrawShapes()


    def RedrawGrid(self):
        self.canvasGrid.ReDraw(int(10 * self.canvasScale))

    def SetTool(self, tool):
        self.tool = tool(self)
    
    def Snap(self, x, y):
        if self.snap:
            x += int(1 * self.canvasScale) 
            y += int(1 * self.canvasScale) 
            x = int(x / (self.canvasScale * 5))
            x = int(x * (self.canvasScale * 5))
            y = int(y / (self.canvasScale * 5))
            y = int(y * (self.canvasScale * 5))
        return x, y

    def Clicked(self, event):
        x, y = self.Snap(event.x, event.y)
        self.tool.Clicked(x, y, self.GetNearestNode(8))
        self.mousePressed = True

    def Released(self, event):
        self.mousePressed = False

    def Motion(self, event):            
        x, y = self.Snap(event.x, event.y)
        self.mousePosition = [x, y]
        self.tool.Hover(x, y)
        self.ShowColision ()

    def RedrawShapes(self):
        for i in range(len(self.drawnShapes)):
            self.drawnShapes[i].Update()

    def GetNearestNode(self, distance):
        nearestNode = None
        for i in range(len(self.drawnShapes)):
            for node in range(len(self.drawnShapes[i].nodes)):
                nodeDistance = abs(math.dist([self.drawnShapes[i].nodes[node].position[0] * self.canvasScale, self.drawnShapes[i].nodes[node].position[1] * self.canvasScale], self.mousePosition))
                if nodeDistance > distance:
                    continue
                if nearestNode == None:
                    nearestNode = (i, node, nodeDistance)
                    continue
                if nearestNode[2] > nodeDistance:
                    nearestNode = (i, node, nodeDistance)
        if nearestNode == None:
            return None
        return self.drawnShapes[nearestNode[0]].nodes[nearestNode[1]]

    def CanvasToMeriCode(self):
        CanvasToMeriCode.CanvasToMeriCode(self)

    def ShowColision(self):
        collidingNode = self.GetNearestNode(8)
        if collidingNode == self.lastCollidedNode and collidingNode != None: #check if the mouse is still on the same node
            return
        if collidingNode == None: # mouse is not on a node so hide the colision circle
            self.selectUIObject.Move(-20, -20)
            return
        self.selectUIObject.SetColor(collidingNode.GetColisionColor())
        self.selectUIObject.Move(int(collidingNode.position[0] * self.canvasScale), int(collidingNode.position[1] * self.canvasScale))

    def LoadSVG(self):
        CanvasSVG.LoadSVG(self)