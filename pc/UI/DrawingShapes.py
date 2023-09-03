from UI.Colors import Colors
from UI.CanvasShapes import CanvasLine
import VectorMath
import math

class Shapes():
    def __init__(self, nodes, canvas):
        self.nodes = nodes
        self.canvas = canvas

    def ReplaceNode(self, nodeToReplace, newNode):
        for i in range(len(self.nodes)):
            if (self.nodes[i] == nodeToReplace):
                self.nodes[i] = newNode

class LinePositions():
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

class Line(Shapes):
    def __init__(self, nodes, canvas, draw = True):
        self.nodes = nodes
        self.canvas = canvas
        self.lines = []

        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)

        if draw:
            self.Draw()

    def Scale(self, scale):
        self.layerScale = scale
        self.Update()

    def Draw(self):
        self.lines.append(CanvasLine(self.canvas, self.nodes[0].GetPositionOnCanvasX(self.canvas), self.nodes[0].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas), Colors.LINECOLOR, 3))

    def Update(self):
        self.lines[0].Move(self.nodes[0].GetPositionOnCanvasX(self.canvas), self.nodes[0].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas))

    def GetStartPosition(self):
        return self.nodes[0].GetPosition()

    def GetEndPosition(self):
        return self.nodes[1].GetPosition()

    def Delete(self):
        for i in range(len(self.lines)):
            self.lines[i].Delete()

        self.lines = []

    #this method will return the actual position of the lines start and end
    def GetLinePositions(self): 
        linePositions = []
        linePositions.append(LinePositions(self.nodes[0].position[0], self.nodes[0].position[1], self.nodes[1].position[0], self.nodes[1].position[1]))
        
        return linePositions



class QuadraticBezier(Shapes): #takes 3 nodes [start, control, end]
    def __init__(self, canvas, nodes, draw = True):
        self.canvas = canvas
        self.nodes = nodes
        self.lines = []
        self.helpLines = []

        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)
        
        if draw:
            self.Draw()

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
        self.DrawHelpLines(useOldLines)
        resolution = int(math.dist(self.nodes[0].GetPosition(), self.nodes[2].GetPosition()) / 3) + 2
        for i in range(resolution + 1):
            if i == 0:
                startNode = VectorMath.QuadraticBezier(self.nodes[0].GetPositionOnCanvas(self.canvas), self.nodes[1].GetPositionOnCanvas(self.canvas), self.nodes[2].GetPositionOnCanvas(self.canvas), i / resolution)
                continue
            endNode = VectorMath.QuadraticBezier(self.nodes[0].GetPositionOnCanvas(self.canvas), self.nodes[1].GetPositionOnCanvas(self.canvas), self.nodes[2].GetPositionOnCanvas(self.canvas), i / resolution)
            if useOldLines and len(self.lines) >= resolution:
                self.lines[i - 1].Move(startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.QBEZIER, 3))

            startNode = endNode

        if len(self.lines) > resolution:
            toDelete = len(self.lines) - resolution
            for i in range(resolution, len(self.lines)):
                self.lines[i].Delete()
            del self.lines[len(self.lines) - toDelete:]

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.nodes[0].GetPositionOnCanvasX(self.canvas), self.nodes[0].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas))
            self.helpLines[1].Move(self.nodes[2].GetPositionOnCanvasX(self.canvas), self.nodes[2].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas))
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].GetPositionOnCanvasX(self.canvas), self.nodes[0].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas), Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].GetPositionOnCanvasX(self.canvas), self.nodes[2].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas), Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)

    def GetStartPosition(self):
        return self.nodes[0].GetPosition()

    def GetEndPosition(self):
        return self.nodes[2].GetPosition()

    def Delete(self):
        for i in range(len(self.lines)):
            self.lines[i].Delete()
            
        for i in range(len(self.helpLines)):
            self.helpLines[i].Delete()
        self.lines = []
        self.helpLines = []

    def GetLinePositions(self): 
        startNode = [0, 0]
        endNode = [0, 0]
        linePositions = []

        resolution = int(math.dist(self.nodes[0].GetPosition(), self.nodes[2].GetPosition()) / 3) + 2
        for i in range(resolution + 1):
            if i == 0:
                startNode = VectorMath.QuadraticBezier(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, i / resolution)
                continue
            endNode = VectorMath.QuadraticBezier(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, i / resolution)
            linePositions.append(LinePositions(startNode[0], startNode[1], endNode[0], endNode[1]))
            startNode = endNode

        return linePositions

class CubicBezier(Shapes): #takes 4 nodes [start, control0, control1, end]
    def __init__(self, canvas, nodes, draw = True):
        self.canvas = canvas
        self.nodes = nodes
        self.lines = []
        self.helpLines = []
        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)
        
        if draw:
            self.Draw()

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
        self.DrawHelpLines(useOldLines)
        resolution = int(math.dist(self.nodes[0].GetPosition(), self.nodes[3].GetPosition()) / 3) + 2

        if len(self.lines) > resolution:
            toDelete = len(self.lines) - resolution
            for i in range(resolution, len(self.lines)):
                self.lines[i].Delete()
            del self.lines[len(self.lines) - toDelete:]

        for i in range(resolution + 1):
            if i == 0:
                startNode = VectorMath.CubicBezier(self.nodes[0].GetPositionOnCanvas(self.canvas), self.nodes[1].GetPositionOnCanvas(self.canvas), self.nodes[2].GetPositionOnCanvas(self.canvas), self.nodes[3].GetPositionOnCanvas(self.canvas), i / resolution)
                continue
            endNode = VectorMath.CubicBezier(self.nodes[0].GetPositionOnCanvas(self.canvas), self.nodes[1].GetPositionOnCanvas(self.canvas), self.nodes[2].GetPositionOnCanvas(self.canvas), self.nodes[3].GetPositionOnCanvas(self.canvas), i / resolution)
            if useOldLines and len(self.lines) >= resolution:
                self.lines[i - 1].Move(startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.CBEZIER, 3))

            startNode = endNode

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.nodes[0].GetPositionOnCanvasX(self.canvas), self.nodes[0].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas))
            self.helpLines[1].Move(self.nodes[2].GetPositionOnCanvasX(self.canvas), self.nodes[2].GetPositionOnCanvasY(self.canvas), self.nodes[3].GetPositionOnCanvasX(self.canvas), self.nodes[3].GetPositionOnCanvasY(self.canvas))
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].GetPositionOnCanvasX(self.canvas), self.nodes[0].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas), Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].GetPositionOnCanvasX(self.canvas), self.nodes[2].GetPositionOnCanvasY(self.canvas), self.nodes[3].GetPositionOnCanvasX(self.canvas), self.nodes[3].GetPositionOnCanvasY(self.canvas), Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)

    def GetStartPosition(self):
        return self.nodes[0].GetPosition()

    def GetEndPosition(self):
        return self.nodes[3].GetPosition()

    def Delete(self):
        for i in range(len(self.lines)):
            self.lines[i].Delete()

        for i in range(len(self.helpLines)):
            self.helpLines[i].Delete()

        self.lines = []
        self.helpLines = []

    #this method will return the actual position of the lines start and end
    def GetLinePositions(self): 
        startNode = [0, 0]
        endNode = [0, 0]
        linePositions = []

        resolution = int(math.dist(self.nodes[0].GetPosition(), self.nodes[3].GetPosition()) / 3) + 2

        for i in range(resolution + 1):
            if i == 0:
                startNode = VectorMath.CubicBezier(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, self.nodes[3].position, i / resolution)
                continue
            endNode = VectorMath.CubicBezier(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, self.nodes[3].position, i / resolution)
            linePositions.append(LinePositions(startNode[0], startNode[1], endNode[0], endNode[1]))

            startNode = endNode
        
        return linePositions

class Arc(Shapes): #takes 3 nodes [start, control, end]
    def __init__(self, canvas, nodes, draw = True):
        self.canvas = canvas
        self.nodes = nodes
        self.lines = []
        self.helpLines = []
        self.radius = 0
        self.resolution = int(math.dist(self.nodes[0].GetPosition(), self.nodes[1].GetPosition()) / 3) + 2
        
        for i in range(len(self.nodes)):
            self.nodes[i].SetShape(self)

        if draw:
            self.Draw()

    def GetArcPoint(self, node0 : tuple, node1 : tuple, node2 : tuple, t):
        x0 = node0[0] #start
        y0 = node0[1]
        x1 = node2[0] #end
        y1 = node2[1]
        x2 = node1[0] #center
        y2 = node1[1]

        r = math.sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0))
        self.radius = r

        startAngle = (math.degrees(math.atan2(y0-y2, x0-x2)))
        endAngle = (math.degrees(math.atan2(y1-y2, x1-x2)))

        if (startAngle < 0):
            startAngle = 180 + (180 - abs(startAngle))

        if (endAngle < 0):
            endAngle = 180 + (180 - abs(endAngle))
        
        if startAngle < endAngle:
            startAngle += 360
        degrees = startAngle - endAngle
        angle = endAngle + (degrees * t)


        if angle > 360:
            angle -= 360
        xP = x2 + r * math.cos(angle * math.pi / 180)
        yP = y2 + r * math.sin(angle * math.pi / 180)

        return [xP, yP]

    def Draw(self, useOldLines = False):
        startNode = [0, 0]
        endNode = [0, 0]
        self.DrawHelpLines(useOldLines)
        for i in range(21):
            if i == 0:
                startNode = self.GetArcPoint(self.nodes[0].GetPositionOnCanvas(self.canvas), self.nodes[1].GetPositionOnCanvas(self.canvas), self.nodes[2].GetPositionOnCanvas(self.canvas), i / 20)
                continue
            endNode = self.GetArcPoint(self.nodes[0].GetPositionOnCanvas(self.canvas), self.nodes[1].GetPositionOnCanvas(self.canvas), self.nodes[2].GetPositionOnCanvas(self.canvas), i / 20)
            if useOldLines:
                self.lines[i - 1].Move(startNode[0], startNode[1], endNode[0], endNode[1])
            else:
                self.lines.append(CanvasLine(self.canvas, startNode[0], startNode[1], endNode[0], endNode[1], Colors.ARC, 3))

            startNode = endNode

    def DrawHelpLines(self, useOldLines = False):
        if useOldLines:
            self.helpLines[0].Move(self.nodes[0].GetPositionOnCanvasX(self.canvas), self.nodes[0].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas))
            self.helpLines[1].Move(self.nodes[2].GetPositionOnCanvasX(self.canvas), self.nodes[2].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas))
            return
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[0].GetPositionOnCanvasX(self.canvas), self.nodes[0].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas), Colors.HELPLINES, 2, (2, 2)))
        self.helpLines.append(CanvasLine(self.canvas, self.nodes[2].GetPositionOnCanvasX(self.canvas), self.nodes[2].GetPositionOnCanvasY(self.canvas), self.nodes[1].GetPositionOnCanvasX(self.canvas), self.nodes[1].GetPositionOnCanvasY(self.canvas), Colors.HELPLINES, 2, (2, 2)))

    def Update(self):
        self.Draw(True)

    def Delete(self):
        for i in range(len(self.lines)):
            self.lines[i].Delete()

        for i in range(len(self.helpLines)):
            self.helpLines[i].Delete()

        self.lines = []
        self.helpLines = []

    #this method will return the actual position of the lines start and end
    def GetLinePositions(self):
        startNode = [0, 0]
        endNode = [0, 0]
        linePositions = []

        for i in range(21):
            if i == 0:
                startNode = self.GetArcPoint(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, i / 20)
                continue
            endNode = self.GetArcPoint(self.nodes[0].position, self.nodes[1].position, self.nodes[2].position, i / 20)
            linePositions.append(LinePositions(startNode[0], startNode[1], endNode[0], endNode[1]))
            startNode = endNode

        return linePositions
    
    def GetStartPosition(self):
        return self.nodes[0].GetPosition()

    def GetEndPosition(self):
        return self.nodes[2].GetPosition()