from UI.Colors import Colors


class Node():
    def __init__(self, x, y, layer):
        self.position = [x / layer.scale, y / layer.scale]
        self.offsetPosition = [0, 0]
        self.connectedNodes = []
        self.shape = None
    
    def UpdateShape(self):
        self.shape.Update()

    def GetShape(self):
        return self.shape

    def SetShape(self, shape):
        self.shape = shape

    def SetScale(self, scaleX, refX, scaleY, refY):
        self.offsetPosition = [(self.position[0] - refX) * scaleX, (self.position[1] - refY) * scaleY]
        self.UpdateShape()

    def GetPosition(self):
        return [self.GetPositionX(), self.GetPositionY()]

    def GetPositionY(self):
        return self.position[1] + self.offsetPosition[1]

    def GetPositionX(self):
        return self.position[0] + self.offsetPosition[0]
    
    @staticmethod
    def GetColisionColor():
        return Colors.COLISIONNODE

class MergedNode():
    def __init__(self, position, nodesToMerge, layer):
        self.position = [position[0] / layer.scale, [1] / layer.scale]
        self.shapes = []
        self.offsetPosition = [0, 0]
        
        for i in range(len(nodesToMerge)):
            self.AddNode(nodesToMerge[i])

    def AddNode(self, nodeToAdd):
        shape = nodeToAdd.GetShape()
        self.shapes.append(shape)
        if shape == None:
            return
        shape.ReplaceNode(nodeToAdd, self)

    def UpdateShape(self):
        for i in range(len(self.shapes)):
            if self.shapes[i] == None:
                continue
            self.shapes[i].Update()

    def SetShape(self, shape):
        self.shapes.append(shape)

    def SetScale(self, scaleX, refX, scaleY, refY):
        self.offsetPosition = [(self.position[0] - refX) * scaleX, (self.position[1] - refY) * scaleY]
        self.UpdateShape()

    def GetPosition(self):
        return [self.GetPositionX(), self.GetPositionY()]

    def GetPositionY(self):
        return self.position[1] + self.offsetPosition[1]

    def GetPositionX(self):
        return self.position[0] + self.offsetPosition[0]

    @staticmethod
    def GetColisionColor():
        return Colors.COLISIONMERGEDNODE
