from UI.Colors import Colors


class Node():
    def __init__(self, x, y):
        self.position = [x, y]
        self.connectedNodes = []
        self.shape = None
    
    def UpdateShape(self):
        self.shape.Update()

    def GetShape(self):
        return self.shape

    def SetShape(self, shape):
        self.shape = shape

    def SetScale(self, scaleX, refX, scaleY, refY):
        self.position[0] += (self.position[0] - refX) * scaleX
        self.position[1] += (self.position[1] - refY) * scaleY
        
        self.UpdateShape()

    def ApplyOffsetPosition(self, x, y):
        self.position[0] += x
        self.position[1] += y

    def GetPosition(self):
        return [self.GetPositionX(), self.GetPositionY()]

    def GetPositionY(self):
        return self.position[1]

    def GetPositionX(self):
        return self.position[0]
    
    @staticmethod
    def GetColisionColor():
        return Colors.COLISIONNODE

class MergedNode():
    def __init__(self, position, nodesToMerge):
        self.position = [position[0], position[1]]
        self.shapes = []
        self.amountNodesMerged = 1
        
        for i in range(len(nodesToMerge)):
            self.AddNode(nodesToMerge[i])

    def AddNode(self, nodeToAdd):
        shape = nodeToAdd.GetShape()
        if shape == None:
            return
        self.shapes.append(shape)
        shape.ReplaceNode(nodeToAdd, self)
        self.amountNodesMerged += 1

    def UpdateShape(self):
        for i in range(len(self.shapes)):
            if self.shapes[i] == None:
                continue
            self.shapes[i].Update()

    def SetShape(self, shape):
        self.shapes.append(shape)

    def SetScale(self, scaleX, refX, scaleY, refY):
        self.position[0] += ((self.position[0] - refX) * scaleX) / self.amountNodesMerged
        self.position[1] += ((self.position[1] - refY) * scaleY) / self.amountNodesMerged
        print(self.amountNodesMerged)
        self.UpdateShape()

    def ApplyOffsetPosition(self, x, y):
        self.position[0] += x / self.amountNodesMerged
        self.position[1] += y / self.amountNodesMerged

    def GetPosition(self):
        return [self.GetPositionX(), self.GetPositionY()]

    def GetPositionY(self):
        return self.position[1]

    def GetPositionX(self):
        return self.position[0]

    @staticmethod
    def GetColisionColor():
        return Colors.COLISIONMERGEDNODE
