import tkinter
import math

from UI.Colors import Colors
import UI.CanvasUI as CanvasUI
import UI.CanvasShapes as CanvasShapes
import UI.DrawingTools as DrawingTools
import UI.CanvasSVG as CanvasSVG

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

        self.tool = DrawingTools.Pen(self)
        self.mousePosition = [0, 0]
        self.drawnShapes = []
        self.lastCollidedNode = None

        self.pixelsPerMM = 10
        self.canvasScale = 1

        self.mousePressed = False
        self.snap = True

        self.gridLines = CanvasUI.DrawGrid(self, self.pixelsPerMM)
        self.selectUIObject = CanvasShapes.CanvasCircle(-20, -20, 8, self)
        self.canvasGridScale = CanvasUI.CanvasGridScale(self, self.pixelsPerMM)

    def Scroll(self, event):
        self.pixelsPerMM += (-1*(event.delta/120)) * 2
        self.canvasScale = self.pixelsPerMM / 10
        if self.pixelsPerMM <= 0:
            self.pixelsPerMM = 2
            self.canvasScale = self.pixelsPerMM / 10
        self.RedrawShapes()
        self.RedrawGrid()

    def RedrawGrid(self):
        for i in range(len(self.gridLines)):
            self.delete(self.gridLines[i])
        if self.canvasScale > 2:
            self.gridLines.extend(CanvasUI.DrawGrid(self, self.pixelsPerMM / 5, "#dddddd"))
        self.gridLines = CanvasUI.DrawGrid(self, int(10 * self.canvasScale))
        self.canvasGridScale = CanvasUI.CanvasGridScale(self, self.pixelsPerMM)
        self.selectUIObject = CanvasShapes.CanvasCircle(-20, -20, 8, self)



    def SetTool(self, name):
        if name == "Pen":
            self.tool = DrawingTools.Pen(self)
            return
        if name == "Move":
            self.tool = DrawingTools.Move(self)
            return
    
    def Snap(self, x, y):
        if self.snap:
            x += int(5 * self.canvasScale) 
            y += int(5 * self.canvasScale) 
            x = int(x / (self.canvasScale * 10))
            x = int(x * (self.canvasScale * 10))
            y = int(y / (self.canvasScale * 10))
            y = int(y * (self.canvasScale * 10))
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
        self.delete("all")
        for i in range(len(self.drawnShapes)):
            self.drawnShapes[i].Draw()

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
                if nearestNode[1] > nodeDistance:
                    nearestNode = (i, node, nodeDistance)
        if nearestNode == None:
            return None
        return self.drawnShapes[nearestNode[0]].nodes[nearestNode[node]]

    def ShowColision(self):
        collidingNode = self.GetNearestNode(8)
        if collidingNode == self.lastCollidedNode and collidingNode != None: #check if the mouse is still on the same node
            return
        if collidingNode == None: # mouse is not on a node so hide the colision circle
            self.selectUIObject.Move(-20, -20)
            return
        self.selectUIObject.SetColor(collidingNode.GetColisionColor())
        self.selectUIObject.Move(int(collidingNode.position[0] * self.canvasScale), int(collidingNode.position[1] * self.canvasScale))

    def CanvasToMeriCode(self):
        with open('Test/MeriCodeTestFile.txt', "w") as file:
            file.write("<S1>" + "\n") #file start command
            for i in range(len(self.drawnShapes)):
                #for now there are only lines
                file.write("<M0 Z" + str(20) + ">" + "\n")
                file.write("<M0 X" + str(self.drawnShapes[i].nodes[0].position[0]) + " Y" + str(self.drawnShapes[i].nodes[0].position[1]) + ">" + "\n") #move the tool to the start of the line
                file.write("<M0 Z" + str(0) + ">" + "\n")
                file.write("<M0 X" + str(self.drawnShapes[i].nodes[1].position[0]) + " Y" + str(self.drawnShapes[i].nodes[1].position[1]) + ">" + "\n") #move the tool to the start of the line
                file.write("<M0 Z" + str(20) + ">" + "\n")
            
            file.write("<M0 X0 Y0>" + "\n") #move the tool in the material
            file.write("<M0 Z0>" + "\n") #move the tool in the material
            file.write("<S0>" + "\n") #file stop command
            file.close()

    def LoadSVG(self):
        CanvasSVG.LoadSVG(self)