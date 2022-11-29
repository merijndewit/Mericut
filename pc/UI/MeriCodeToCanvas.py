from MeriCode.FileToMeriCode import FileToMeriCode
import UI.CanvasShapes as CanvasShapes
import re

class MeriCodeToCanvas:
    def __init__(self, layer, cutting):
        self.position = [0.0, 0.0, 0.0] #x, y and z
        self.rotation = 0
        self.layer = layer
        self.cutting = cutting
        self.toolOffsetRadius = 3.5
        self.zUpPosition = 20

    def DrawMeriCode(self):
        file = FileToMeriCode.GetMeriCodeFromTxt()
        for i in range(len(file)):
            start = '<'
            end = '>'
            self.ExecuteCallbackCode(file[i][file[i].find(start)+len(start):file[i].rfind(end)])

    def ExecuteCallbackCode(self, meriCode :str):
        if meriCode[0] == 'M':
            self.ExecuteMcode(meriCode[1:])

    def ExecuteMcode(self, meriCode :str):
        number = re.search(r'\d+', meriCode).group()
        if number == '0' or number == '1':
            self.Move(meriCode[2:])

    def Move(self, meriCode :str):
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
        print(x, self.position[0])
        if x == self.position[0] and y == self.position[1]:
            return

        travel = False   
        if self.position[2] == self.zUpPosition:
            travel = True
        self.DrawLine([x, y], travel)

        self.position[0] = x
        self.position[1] = y

    def DrawLine(self, nextPosition, travel :bool):
        color = "#FF0000"
        if travel: 
            color = "#00FF00"
        print(color)
        self.layer.AddShape(CanvasShapes.CanvasLine(self.layer.canvas, self.position[0], self.position[1], nextPosition[0], nextPosition[1], color, scaleWithCanvas=True))
            