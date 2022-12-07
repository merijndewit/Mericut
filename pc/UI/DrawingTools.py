import UI.DrawingShapes as DrawingShapes
import UI.CanvasShapes as CanvasShapes

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

    def Clicked(self, x, y, clickedNode, clickedLayer):
        nodePositionX = (x / self.parentCanvas.canvasScale)
        nodePositionY = (y / self.parentCanvas.canvasScale)
        if clickedNode == None: #not clicked on any nodes
            self.nodes.append(Nodes.Node(nodePositionX, nodePositionY))
        elif (isinstance(clickedNode, Nodes.Node)): #clicked on a node
            #self.nodes.append(Nodes.MergedNode(clickedNode.position, [clickedNode, Nodes.Node(nodePositionX, nodePositionY)]))
            self.nodes.append(Nodes.Node(clickedNode.GetPositionX(), clickedNode.GetPositionY()))
        else: #clicked on a merged node
            clickedNode.AddNode(Nodes.Node(x, y))
            self.nodes.append(clickedNode)
        if self.clicks == 1:
            line = DrawingShapes.Line(self.nodes, self.parentCanvas)
            self.parentCanvas.selectedLayer.AddShape(line)
            self.clicks = 0
            self.nodes = []
            self.parentCanvas.delete(self.previewLine.canvasLine)
            self.previewLine = None
            return

        self.clicks += 1

    def Hover(self, x, y):
        x = (x + self.parentCanvas.xOffset)
        y = (y + self.parentCanvas.yOffset)
        if self.clicks == 1:
            if self.previewLine == None:
                self.previewLine = CanvasShapes.CanvasLine(self.parentCanvas, self.nodes[0].GetPositionOnCanvasX(self.parentCanvas), self.nodes[0].GetPositionOnCanvasY(self.parentCanvas), (x / self.parentCanvas.canvasScale) + self.parentCanvas.xOffset, (y / self.parentCanvas.canvasScale) + self.parentCanvas.yOffset)
                return
            self.previewLine.Move(self.nodes[0].GetPositionOnCanvasX(self.parentCanvas), self.nodes[0].GetPositionOnCanvasY(self.parentCanvas), (x), (y))
            return

class Move(Tool):
    def __init__(self, parentCanvas):
        super().__init__(parentCanvas)
        self.clickedPosition = [0, 0]
        self.lastMoved = [0, 0]
        self.clickedOffset = [0, 0]


    def Clicked(self, x, y, clickedNode, clickedLayer):
        self.clickedNode = clickedNode
        self.clickedLayer = clickedLayer
        self.clickedPosition = [x, y]
        self.lastMoved = [0, 0]
        self.clickedOffset = [self.parentCanvas.xOffset, self.parentCanvas.yOffset]

    def Hover(self, x, y):
        nodePositionX = x / self.parentCanvas.canvasScale
        nodePositionY = y / self.parentCanvas.canvasScale
        if self.parentCanvas.mousePressed and self.clickedNode != None:
            self.clickedNode.position = [nodePositionX, nodePositionY]
            self.clickedNode.UpdateShape()
            return
        elif self.parentCanvas.mousePressed and self.clickedLayer:
            self.parentCanvas.selectedLayer.Move([x, y])
        elif self.parentCanvas.mousePressed:
            self.parentCanvas.MoveView((x - self.clickedPosition[0]), (y - self.clickedPosition[1]))
        self.clickedNode = None

class QuadraticBezier(Tool):
    def __init__(self, parentCanvas):
        super().__init__(parentCanvas)
        self.previewLine = None

    def Clicked(self, x, y, clickedNode, clickedLayer):
        self.DrawCurve()

    def Hover(self, x, y):
        return

    def DrawCurve(self):
        curve = DrawingShapes.QuadraticBezier(self.parentCanvas, [Nodes.Node(20, 20), Nodes.Node(30, 30), Nodes.Node(20, 40)])
        self.parentCanvas.selectedLayer.AddShape(curve)

class CubicBezier(Tool):
    def __init__(self, parentCanvas):
        super().__init__(parentCanvas)
        self.previewLine = None

    def Clicked(self, x, y, clickedNode, clickedLayer):
        self.DrawCurve()

    def Hover(self, x, y):
        return

    def DrawCurve(self):
        curve = DrawingShapes.CubicBezier(self.parentCanvas, [Nodes.Node(20, 20), Nodes.Node(30, 30), Nodes.Node(20, 40), Nodes.Node(40, 40)])
        self.parentCanvas.selectedLayer.AddShape(curve)


class Arc(Tool):
    def __init__(self, parentCanvas):
        super().__init__(parentCanvas)
        self.previewLine = None

    def Clicked(self, x, y, clickedNode, clickedLayer):
        self.DrawCurve()

    def Hover(self, x, y):
        return

    def DrawCurve(self):
        curve = DrawingShapes.Arc(self.parentCanvas, [Nodes.Node(20, 20), Nodes.Node(30, 30), Nodes.Node(20, 40)])
        self.parentCanvas.selectedLayer.AddShape(curve)


