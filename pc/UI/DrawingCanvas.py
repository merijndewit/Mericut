import tkinter
import math

from UI.Colors import Colors
import UI.CanvasUI as CanvasUI
import UI.CanvasShapes as CanvasShapes
import UI.DrawingTools as DrawingTools
import UI.CanvasSVG as CanvasSVG
import UI.CanvasToMeriCode as CanvasToMeriCode
import UI.Layer as Layer

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
        self.selectedLayer = Layer.Layer(self, "layer")
        self.layers = [self.selectedLayer]
        self.lastCollidedNode = None
        self.background = None

        self.pixelsPerMM = 10
        self.canvasScale = 1
        self.xOffset = 0
        self.yOffset = 0

        self.mousePressed = False
        self.snap = True

        self.canvasGrid = CanvasUI.CanvasGrid(self, self.pixelsPerMM)
        self.selectUIObject = CanvasShapes.CanvasCircle(-20, -20, 8, self)

        self.lastSnapPosition = [0, 0]

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
        if self.background is not None:
            self.background.Delete()
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
        self.background = CanvasShapes.CanvasRectangle(width, height, self, tags="background")
        self.background.SetColor(color)
        self.background.SetScale(self.canvasScale)
        self.tag_lower("background")

    def MoveView(self, x, y):
        self.xOffset += x
        self.yOffset += y
        self.RedrawGrid()
        self.RedrawShapes()
        self.selectedLayer.CanvasScaleChanged()

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
        self.selectedLayer.CanvasScaleChanged()


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
        x -= self.xOffset
        y -= self.yOffset
        self.tool.Clicked(x, y, self.selectedLayer.GetCollidingNode(8, self.canvasScale, self.mousePosition), self.selectedLayer.IsColliding([x / self.canvasScale, y / self.canvasScale]))
        self.mousePressed = True

    def Released(self, event):
        self.mousePressed = False

    def Motion(self, event):            
        x, y = self.Snap(event.x, event.y)
        x -= self.xOffset
        y -= self.yOffset
        self.lastSnapPosition = [x, y]
        self.mousePosition = [event.x - self.xOffset, event.y - self.yOffset]
        self.tool.Hover(x, y)
        self.ShowColision()

    def RedrawShapes(self):
        for i in range(len(self.layers)):
            self.layers[i].RedrawShapes()

    def CanvasToMeriCode(self, cutting):
        CanvasToMeriCode.CanvasToMeriCode(self, cutting)

    def ShowColision(self):
        collidingNode = self.selectedLayer.GetCollidingNode(8, self.canvasScale, self.mousePosition)
        if collidingNode == self.lastCollidedNode and collidingNode != None: #check if the mouse is still on the same node
            return
        if collidingNode == None: # mouse is not on a node so hide the colision circle
            self.selectUIObject.Move(-20, -20)
            return
        self.selectUIObject.SetColor(collidingNode.GetColisionColor())
        self.selectUIObject.Move(int((collidingNode.GetPositionX() * self.canvasScale) + self.xOffset), int((collidingNode.GetPositionY() * self.canvasScale) + self.yOffset))

    def LoadSVG(self, dir):
        CanvasSVG.LoadSVG(self, dir)

    def SaveSVG(self):
        CanvasSVG.SaveSVG(self)

    def GetLayerNames(self):
        names = []
        for i in range(len(self.layers)):
            names.append(self.layers[i].name)
        return names

    def SelectLayer(self, name):
        for i in range(len(self.layers)):
            if self.layers[i].name == name:
                self.selectedLayer.StopResizing()
                self.selectedLayer = self.layers[i]
                return

    def TransformLayer(self, name):
        for i in range(len(self.layers)):
            if self.layers[i].name == name:
                self.selectedLayer = self.layers[i]
                if self.selectedLayer.resizing:
                    self.selectedLayer.StopResizing()
                    return
                self.selectedLayer.StartResizing()
                return

    def AddLayer(self, name="layer"):
        number = 0
        foundName = False
        while foundName == False:
            foundName = True
            for i in range(len(self.layers)):
                if self.layers[i].name == name:
                    if name.endswith(str(number - 1)):
                        name = name[:-1] + str(number)
                    else:
                        name += str(number)
                    number += 1
                    foundName = False
                    break
            
        newLayer = Layer.Layer(self, name)
        self.layers.append(newLayer)
        self.selectedLayer = newLayer
        self.parent.parent.canvasLayerFrame.AddLayerButton(name)

    def DeleteLayer(self, name):
        for i in range(len(self.layers)):
            if self.layers[i].name == name:
                self.layers[i].Delete()
                self.layers.remove(self.layers[i])
                break

        if len(self.layers) == 0:
            self.AddLayer()
            return
        self.selectedLayer = self.layers[0]
            
