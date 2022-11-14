import math
from UI.Nodes import Node
from UI.CanvasShapes import CanvasCircle

class Layer():
    def __init__(self, canvas, name):
        self.name = name
        self.canvas = canvas
        self.drawnShapes = [] 
        self.resizeNodes = [None, None]
        self.sizeShapes = []
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
        nodesToCheck = [self.resizeNodes[1]]
        if self.resizing: #check Nodes
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
            
        for i in range(len(self.drawnShapes)): #check shapes
            for node in range(len(self.drawnShapes[i].nodes)):
                nodeDistance = abs(math.dist([self.drawnShapes[i].nodes[node].position[0] * canvasScale, self.drawnShapes[i].nodes[node].position[1] * canvasScale], mousePosition))
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

    def AddShape(self, shape):
        self.drawnShapes.append(shape)

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
        currentWidth = (self.resizeNodes[0].position[0] / self.canvas.canvasScale) - (self.resizeNodes[1].position[0] / self.canvas.canvasScale)
        #currentHeight = (self.resizeNodes[0].position[1] / self.canvas.canvasScale) - (self.resizeNodes[1].position[1] / self.canvas.canvasScale)
        currentWidth /= self.canvas.canvasScale
        scaleX = ((currentWidth - self.startWidth) / self.startWidth)
        #scaleY = ((currentHeight - self.startHeight) / self.startHeight)
        tolerance = 0.04

        self.sizeShapes[0].Move(self.resizeNodes[0].position[0] * self.canvas.canvasScale, self.resizeNodes[0].position[1] * self.canvas.canvasScale)
        self.sizeShapes[1].Move(self.resizeNodes[1].position[0] * self.canvas.canvasScale, self.resizeNodes[1].position[1] * self.canvas.canvasScale)

        self.ApplyScale(scaleX, scaleX)
     
    def StartResizing(self):
        if self.resizeNodes[0] == None or self.resizeNodes[0] == None:
            self.StopResizing()
            nodePositions = self.GetBorderPositions()
            self.resizeNodes[0] = (Node(nodePositions[0][0], nodePositions[0][1], self))
            self.resizeNodes[1] = (Node(nodePositions[1][0], nodePositions[1][1], self))
            self.resizeNodes[0].SetShape(self)
            self.resizeNodes[1].SetShape(self)
            self.sizeShapes.append(CanvasCircle(self.resizeNodes[0].position[0], self.resizeNodes[0].position[1], 5, self.canvas))
            self.sizeShapes.append(CanvasCircle(self.resizeNodes[1].position[0], self.resizeNodes[1].position[1], 5, self.canvas))
        else:
            self.sizeShapes[1].Move(self.resizeNodes[1].position[0] * self.canvas.canvasScale, self.resizeNodes[1].position[1] * self.canvas.canvasScale)
            self.sizeShapes[0].Move(self.resizeNodes[0].position[0] * self.canvas.canvasScale, self.resizeNodes[0].position[1] * self.canvas.canvasScale)

        self.resizing = True
        self.startWidth = (self.resizeNodes[0].position[0] / self.canvas.canvasScale) - (self.resizeNodes[1].position[0] / self.canvas.canvasScale)
        self.startHeight = (self.resizeNodes[0].position[0] / self.canvas.canvasScale - self.resizeNodes[1].position[0] / self.canvas.canvasScale)

    def StopResizing(self):
        for i in range(len(self.sizeShapes)):
            self.sizeShapes[i].Delete()

        self.sizeShapes = []
        self.resizing = False

    def CanvasScaleChanged(self):
        if self.resizing == False:
            return    
        #for i in range(len(self.sizeShapes)):
        #    self.sizeShapes[i].SetScale(self.canvas.canvasScale)
        if self.resizing:
            self.StartResizing()
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

        



