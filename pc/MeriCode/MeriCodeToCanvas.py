from MeriCode.FileToMeriCode import FileToMeriCode
import UI.CanvasShapes as CanvasShapes
import re
import math
import UI.DrawingShapes as DrawingShapes
import UI.Nodes as Nodes

class MeriCodeToCanvas:
    def __init__(self, canvasManager):
        self.position = [0.0, 0.0, 0.0] #x, y and z
        self.rotation = 0
        self.layer = None
        self.cutting = False
        self.toolOffsetRadius = 3.75
        self.zUpPosition = 20
        self.lines = []
        self.canvasManager = canvasManager

    def DrawMeriCode(self, layer, cutting):
        self.layer = layer
        self.cutting = cutting
        file = FileToMeriCode.GetMeriCodeFromTxt()
        self.lines = []
        for i in range(len(file)):
            start = '<'
            end = '>'
            self.__ExecuteCallbackCode__(file[i][file[i].find(start)+len(start):file[i].rfind(end)])

    def ShowSingleMeriCodeLine(self, line :int):
        if len(self.lines) == 0 or len(self.lines) - 1 < line:
            return
        self.lines[line].Draw()
        self.layer.AddShape(self.lines[line])

    def __ExecuteCallbackCode__(self, meriCode :str):
        if meriCode[0] == 'M':
            self.__ExecuteMcode__(meriCode[1:])

    def __ExecuteMcode__(self, meriCode :str):
        number = re.search(r'\d+', meriCode).group()
        if number == '0' or number == '1':
            self.__Move__(meriCode[2:])

    def __Move__(self, meriCode :str):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        if re.search('X', meriCode) is not None:
            x = float(re.search('X([0-9.-]+)', meriCode)[1])

        if re.search('Y', meriCode) is not None:
            y = float(re.search('Y([0-9.-]+)', meriCode)[1])

        if re.search('Z', meriCode) is not None:
            z = float(re.search('Z([0-9.-]+)', meriCode)[1])
            self.position[2] = z

        if re.search('T', meriCode) is not None:
            self.rotation = float(re.search('T([0-9.-]+)', meriCode)[1])
        
        if x == self.position[0] and y == self.position[1]:
            return

        if self.cutting:
            offsetPosition = self.__GetOffsetPosition__(self.toolOffsetRadius, self.rotation)
            if x != None:
                x -= offsetPosition[0]

            if y != None:
                y -= offsetPosition[1]

        travel = False   
        if self.position[2] == self.zUpPosition:
            travel = True

        self.__DrawLine__([x, y], travel)

        self.position[0] = x
        self.position[1] = y

    def __DrawLine__(self, nextPosition, travel :bool):
        color = "#FF0000"
        if travel: 
            color = "#00FF00"
        line = DrawingShapes.Line((Nodes.Node(self.position[0], self.position[1]), Nodes.Node(nextPosition[0], nextPosition[1])), self.canvasManager, color)
        self.lines.append(line)
        self.layer.AddShape(line)
            
    @staticmethod
    def __GetOffsetPosition__(radius, angle):
        invert = True
        angle = math.radians(angle)

        x = radius * math.sin(angle)
        if invert and x < 0:
            x = abs(x)
        else:
            x = -abs(x)

        y = radius * math.cos(angle)
        if invert and y < 0:
            y = abs(y)
        else:
            y = -abs(y)

        return [y, x]