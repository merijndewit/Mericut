import math
from UI.Nodes import Node
from UI.CanvasShapes import CanvasCircle

class Layer():
    def __init__(self, canvas, name):
        self.name = name
        self.canvas = canvas
        self.drawnShapes = [] 
        self.resizeNodes = [Node(-100, -100, self), Node(-100, -100, self)]
        self.sizeShapes = [CanvasCircle(-100, -100, 5, self.canvas), CanvasCircle(-100, -100, 5, self.canvas)]
        self.resizeNodes[0].SetShape(self)
        self.resizeNodes[1].SetShape(self)
        self.resizing = False

        #resizing borders
        self.startWidth = 0
        self.startHeight = 0

        #scaling for shapes only assigned to this layer
        self.scale = 1

        #moving
        self.lastMovedPositionX = None
        self.lastMovedPositionY = None

    def RedrawShapes(self):
        for i in range(len(self.drawnShapes)):
            self.drawnShapes[i].Update()

    def GetCollidingNode(self, distance, canvasScale, mousePosition):
        nearestNode = None
        nodesToCheck = []
        if self.resizing: 
            nodesToCheck = [self.resizeNodes[1]]
        else:
            for i in range(len(self.drawnShapes)): #check shapes
                for node in range(len(self.drawnShapes[i].nodes)):
                    nodesToCheck.append(self.drawnShapes[i].nodes[node])

        for node in range(len(nodesToCheck)):
            nodeDistance = abs(math.dist([nodesToCheck[node].position[0] * canvasScale, nodesToCheck[node].position[1] * canvasScale], mousePosition))
            if nodeDistance > distance:
                continue
            if nearestNode == None:
                nearestNode = (node,nodeDistance)
                continue
            if nearestNode[1] > nodeDistance:
                nearestNode = (node,nodeDistance)
        if nearestNode == None:
            return None
        return nodesToCheck[nearestNode[0]]

    def AddShape(self, shape):
        self.drawnShapes.append(shape)
        for i in range(len(shape.nodes)):
            shape.nodes[i].position = [shape.nodes[i].position[0] / self.scale, shape.nodes[i].position[1] / self.scale]

    def ApplyScale(self, scaleX, scaleY):
        for shape in range(len(self.drawnShapes)):
            for node in range(len(self.drawnShapes[shape].nodes)):
                    self.drawnShapes[shape].nodes[node].SetScale(scaleX, self.resizeNodes[0].position[0], scaleY, self.resizeNodes[0].position[1])
        self.RedrawShapes()

    def AddTransform(self, x, y):
        for shape in range(len(self.drawnShapes)):
            for node in range(len(self.drawnShapes[shape].nodes)):
                xNode = self.drawnShapes[shape].nodes[node].position[0]
                yNode = self.drawnShapes[shape].nodes[node].position[1]
                self.drawnShapes[shape].nodes[node].position = [xNode + x, yNode + y]
        self.RedrawShapes()

    
    def GetBorderPositions(self):
        minX = math.inf
        minY = math.inf
        maxX = 0
        maxY = 0
        for shape in range(len(self.drawnShapes)):
            for node in range(len(self.drawnShapes[shape].nodes)):
                position = self.drawnShapes[shape].nodes[node].position
                if position[0] < minX:
                    minX = position[0]
                elif position[0] > maxX:
                    maxX = position[0]

                if position[1] < minY:
                    minY = position[1]
                elif position[1] > maxY:
                    maxY = position[1]
        return [[minX, minY], [maxX, maxY]]
    
    def Update(self):
        currentWidth = self.resizeNodes[0].position[0] - self.resizeNodes[1].position[0]
        scaleX = (((currentWidth) / self.startWidth) * 100)
        scaleX /= 100
        scaleX -= 1
        self.sizeShapes[0].Move(self.resizeNodes[0].position[0] * self.canvas.canvasScale, self.resizeNodes[0].position[1] * self.canvas.canvasScale)
        self.sizeShapes[1].Move(self.resizeNodes[1].position[0] * self.canvas.canvasScale, self.resizeNodes[1].position[1] * self.canvas.canvasScale)
        self.scale = scaleX + 1
        self.ApplyScale(scaleX, scaleX)
     
    def StartResizing(self):
        nodePositions = self.GetBorderPositions()
        self.resizeNodes[0].position = [nodePositions[0][0], nodePositions[0][1]]
        self.resizeNodes[1].position = [nodePositions[1][0], nodePositions[1][1]]
        self.sizeShapes[1].Move(self.resizeNodes[1].position[0] * self.canvas.canvasScale, self.resizeNodes[1].position[1] * self.canvas.canvasScale)
        self.sizeShapes[0].Move(self.resizeNodes[0].position[0] * self.canvas.canvasScale, self.resizeNodes[0].position[1] * self.canvas.canvasScale)

        self.startWidth = (self.resizeNodes[0].position[0]) - (self.resizeNodes[1].position[0])
        self.startHeight = (self.resizeNodes[0].position[0]) - (self.resizeNodes[1].position[0])
        self.resizing = True

    def StopResizing(self):
        self.sizeShapes[1].Move(-100, -100)
        self.sizeShapes[0].Move(-100, -100)
        self.resizing = False

    def CanvasScaleChanged(self):
        self.sizeShapes[0].Move(self.resizeNodes[0].position[0] * self.canvas.canvasScale, self.resizeNodes[0].position[1] * self.canvas.canvasScale)
        self.sizeShapes[1].Move(self.resizeNodes[1].position[0] * self.canvas.canvasScale, self.resizeNodes[1].position[1] * self.canvas.canvasScale)

    def IsColliding(self, position):
        if self.resizing == False:
            return False    
        if position[0] > self.resizeNodes[0].position[0] and position[0] < self.resizeNodes[1].position[0]:
            if position[1] > self.resizeNodes[0].position[1] and position[1] < self.resizeNodes[1].position[1]:
                return True
        return False

    def Move(self, position):
        position[0] /= self.canvas.canvasScale
        position[1] /= self.canvas.canvasScale

        if self.lastMovedPositionX == None:
            self.lastMovedPositionX = position[0]
            self.lastMovedPositionY = position[1]
            return
        moved = [position[0] - self.lastMovedPositionX, position[1] - self.lastMovedPositionY]
        self.AddTransform(moved[0], moved[1])
        self.lastMovedPositionX = position[0]
        self.lastMovedPositionY = position[1]

        self.resizeNodes[0].position[0] += moved[0]
        self.resizeNodes[0].position[1] += moved[1]
        self.resizeNodes[1].position[0] += moved[0]
        self.resizeNodes[1].position[1] += moved[1]


        self.sizeShapes[0].Move(self.resizeNodes[0].position[0] * self.canvas.canvasScale, self.resizeNodes[0].position[1] * self.canvas.canvasScale)
        self.sizeShapes[1].Move(self.resizeNodes[1].position[0] * self.canvas.canvasScale, self.resizeNodes[1].position[1] * self.canvas.canvasScale)

        



