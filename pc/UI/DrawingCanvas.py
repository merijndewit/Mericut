import tkinter
import math

from UI.Colors import Colors
import UI.CanvasUI as CanvasUI
import UI.CanvasShapes as CanvasShapes
import UI.DrawingTools as DrawingTools
import UI.CanvasSVG as CanvasSVG
import MeriCode.CanvasToMeriCode as CanvasToMeriCode
import UI.Layer as Layer
import MeriCode.MeriCodeToCanvas as MeriCodeToCanvas

class DrawingCanvas():
    def __init__(self, parent):
        self.parent = parent

        self.tool = DrawingTools.Pen(self)
        self.mousePosition = [0, 0]
        self.selectedLayer = Layer.Layer(self, "layer")
        self.mericodeToCanvas = MeriCodeToCanvas.MeriCodeToCanvas()
        self.layers = [self.selectedLayer]
        self.lastCollidedNode = None
        self.background = None

        self.pixelsPerMM = 10
        self.canvasScale = 1
        self.screenOffsetX = 0
        self.screenOffsetY = 0

        self.mousePressed = False
        self.snap = True

        self.canvasGrid = CanvasUI.CanvasGrid(self, self.pixelsPerMM, self.screenOffsetX, self.screenOffsetY)
        self.selectUIObject = CanvasShapes.CanvasCircle(-20, -20, 8, self, Colors.COLISIONNODE)

        self.lastSnapPosition = [0, 0]

        self.canvasToMericode = None

    def ResizedWindow(self,event):
        width = event.width
        height = event.height

        self.config(width=width, height=height)
        if self.background is not None:
            self.background.Update([self.screenOffsetX, self.screenOffsetY], self.canvasScale)

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
        self.background = CanvasShapes.CanvasRectangle([self.screenOffsetX, self.screenOffsetY], width, height, self, tags="background")
        self.background.SetColor(color)
        self.background.Update([self.screenOffsetX, self.screenOffsetY], self.canvasScale)
        self.tag_lower("background")

    def MoveView(self, x, y):
        self.screenOffsetX += x
        self.screenOffsetY += y
        self.RedrawGrid()
        self.RedrawShapes()
        self.selectedLayer.CanvasScaleChanged()
        if self.background is not None:
            self.background.Update([self.screenOffsetX, self.screenOffsetY], self.canvasScale)

    def Scroll(self, scroll : int):
        self.pixelsPerMM += (-1*(scroll/20)) * 2
        self.canvasScale = self.pixelsPerMM / 10
        if self.pixelsPerMM <= 0:
            self.pixelsPerMM = 2
            self.canvasScale = self.pixelsPerMM / 10
        if self.background is not None:
            self.background.Update([self.screenOffsetX, self.screenOffsetY], self.canvasScale)
        self.ClearCanvas()
        self.RedrawGrid()
        self.RedrawShapes()
        self.selectedLayer.CanvasScaleChanged()

    def ClearCanvas(self):
        self.parent.Clear()

    def RedrawGrid(self):
        self.canvasGrid.ReDraw(10 * self.canvasScale, self.screenOffsetX, self.screenOffsetY)

    def SetTool(self, tool):
        self.tool = tool(self)
    
    def Snap(self, x, y):
        if self.snap:
            x += int(1 * self.canvasScale) 
            y += int(1 * self.canvasScale) 
            x = int(x / (self.canvasScale * 1))
            x = int(x * (self.canvasScale * 1))
            y = int(y / (self.canvasScale * 1))
            y = int(y * (self.canvasScale * 1))
        return x, y

    def Clicked(self, xInput, yInput):
        x, y = self.Snap(xInput, yInput)
        x -= self.screenOffsetX
        y -= self.screenOffsetY
        self.tool.Clicked(x, y, self.selectedLayer.GetCollidingNode(8, self.canvasScale, self.mousePosition), self.selectedLayer.IsColliding([x / self.canvasScale, y / self.canvasScale]))
        self.mousePressed = True

    def Released(self):
        self.mousePressed = False

    def Motion(self, xInput, yInput):            
        x, y = self.Snap(xInput, yInput)
        x -= self.screenOffsetX
        y -= self.screenOffsetY
        self.lastSnapPosition = [x, y]
        self.mousePosition = [xInput - self.screenOffsetX, yInput - self.screenOffsetY]
        self.tool.Hover(x, y)
        self.ShowColision()

    def RedrawShapes(self):
        for i in range(len(self.layers)):
            self.layers[i].RedrawShapes()

    def CanvasToMeriCode(self):
        self.canvasToMericode = CanvasToMeriCode.CanvasToMeriCode(self, self.parent.parent.mericodeSlicingOptions)

    def ShowColision(self):
        collidingNode = self.selectedLayer.GetCollidingNode(8, self.canvasScale, self.mousePosition)
        if collidingNode == self.lastCollidedNode and collidingNode != None: #check if the mouse is still on the same node
            self.parent.Clear()
            self.RedrawGrid()
            self.RedrawShapes()
            return
        if collidingNode == None: # mouse is not on a node so hide the colision circle
            self.parent.Clear()
            self.RedrawGrid()
            self.RedrawShapes()
            return
        self.parent.Clear()
        self.RedrawGrid()
        self.RedrawShapes()
        self.selectUIObject.Move(collidingNode.GetPositionOnCanvasX(self), collidingNode.GetPositionOnCanvasY(self))

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

    def CanvasPosXToNormalPosX(self, x):
        return (x / self.canvasScale) - self.screenOffsetX
    
    def CanvasPosYToNormalPosY(self, y):
        return (y / self.canvasScale) - self.screenOffsetY

    def ShowMeriCode(self, cutting :bool):
        for i in range(len(self.layers)):
            if self.layers[i].name == "Movement":
                self.layers[i].Delete()
                self.SelectLayer("Movement")
                break
        else:
            self.AddLayer("Movement")

        self.mericodeToCanvas.DrawMeriCode(self.selectedLayer, cutting)

    def ShowSingleMeriCodeLine(self, line :int):
        for i in range(len(self.layers)):
            if self.layers[i].name == "Movement":
                self.layers[i].Delete()
                self.SelectLayer("Movement")
                break
        else:
            self.AddLayer("Movement")

        self.mericodeToCanvas.ShowSingleMeriCodeLine(line)

    def ConvertPositionToScreenPosition(self, position : tuple):
        return [self.screenOffsetX + position[0], self.screenOffsetY + position[1]]
