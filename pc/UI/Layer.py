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
        self.startWidth = 0
        self.startHeight = 0
        self.scale = 1

    def RedrawShapes(self):
        for i in range(len(self.drawnShapes)):
            self.drawnShapes[i].Update()

    def GetCollidingNode(self, distance, canvasScale, mousePosition):
        nearestNode = None
        if self.resizing:
            for node in range(len(self.resizeNodes)):
                nodeDistance = abs(math.dist([self.resizeNodes[node].position[0] * canvasScale, self.resizeNodes[node].position[1] * canvasScale], mousePosition))
                if nodeDistance > distance:
                    continue
                if nearestNode == None:
                    nearestNode = (node,nodeDistance)
                    continue
                if nearestNode[1] > nodeDistance:
                    nearestNode = (node,nodeDistance)
            if nearestNode == None:
                return None
            return self.resizeNodes[nearestNode[0]]
            
        for i in range(len(self.drawnShapes)):
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

    def ApplyScale(self, differenceX, differenceY):
        for shape in range(len(self.drawnShapes)):
            for node in range(len(self.drawnShapes[shape].nodes)):
                self.drawnShapes[shape].nodes[node].SetScale(differenceX, self.resizeNodes[0].position[0], differenceY, self.resizeNodes[0].position[1])
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
        return [[minX - 5, minY - 5], [maxX + 5, maxY + 5]]
    
    def Update(self):
        currentWidth = (self.resizeNodes[0].position[0] / self.canvas.canvasScale - self.resizeNodes[1].position[0] / self.canvas.canvasScale)
        differenceX = (abs(currentWidth - self.startWidth) / self.startWidth)
        differenceY = (abs(currentWidth - self.startWidth) / self.startWidth)

        self.sizeShapes[0].Move(self.resizeNodes[0].position[0] * self.canvas.canvasScale, self.resizeNodes[0].position[1] * self.canvas.canvasScale)
        self.sizeShapes[1].Move(self.resizeNodes[1].position[0] * self.canvas.canvasScale, self.resizeNodes[1].position[1] * self.canvas.canvasScale)

        #print("difference " + str((differenceX)))

        self.ApplyScale(differenceX, differenceY)
                
    def Resize(self):
        self.StopResizing()
        nodePositions = self.GetBorderPositions()
        self.resizeNodes[0] = (Node(nodePositions[0][0], nodePositions[0][1], self))
        self.resizeNodes[1] = (Node(nodePositions[1][0], nodePositions[1][1], self))
        self.resizeNodes[0].SetShape(self)
        self.resizeNodes[1].SetShape(self)
        self.sizeShapes.append(CanvasCircle(self.resizeNodes[0].position[0], self.resizeNodes[0].position[1], 5, self.canvas))
        self.sizeShapes.append(CanvasCircle(self.resizeNodes[1].position[0], self.resizeNodes[1].position[1], 5, self.canvas))
        self.resizing = True
        self.startWidth = (self.resizeNodes[0].position[0] - self.resizeNodes[1].position[0])
        self.startHeight = (self.resizeNodes[0].position[0] - self.resizeNodes[1].position[0])


    def StopResizing(self):
        for i in range(len(self.sizeShapes)):
            self.sizeShapes[i].Delete()

        self.sizeShapes = []

    def CanvasScaleChanged(self):
        if self.resizing == False:
            return    
        for i in range(len(self.sizeShapes)):
            self.sizeShapes[i].SetScale(self.canvas.canvasScale)


