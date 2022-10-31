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
    @staticmethod
    def GetColisionColor():
        return Colors.COLISIONNODE

class MergedNode():
    def __init__(self, position, nodesToMerge):
        self.position = position
        self.shapes = []
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
    @staticmethod
    def GetColisionColor():
        return Colors.COLISIONMERGEDNODE
