import math
class CanvasToMeriCode:
    def __init__(self, canvas, cutting):
        self.position = [0, 0]
        self.canvas = canvas
        self.mergeDistance = 0.04
        self.cutting = cutting
        self.toolOffsetRadius = 4
        with open('Test/MeriCodeTestFile.txt', "w") as file:
            for layer in range(len(self.canvas.layers)):
                for i in range(len(self.canvas.layers[layer].drawnShapes)):
                    shapeStartPosition = self.canvas.layers[layer].drawnShapes[i].GetStartPosition()
                    shapeEndPosition = self.canvas.layers[layer].drawnShapes[i].GetEndPosition()
                    if (abs(self.position[0] - shapeStartPosition[0]) <= self.mergeDistance and abs(self.position[1] - shapeStartPosition[1]) <= self.mergeDistance):
                        self.DrawShapeReversed(file, self.canvas.layers[layer].drawnShapes[i].lines)
                        continue
                    if (abs(self.position[0] - shapeEndPosition[0]) <= self.mergeDistance and abs(self.position[1] - shapeEndPosition[1]) <= self.mergeDistance):
                        self.DrawShape(file, self.canvas.layers[layer].drawnShapes[i].lines)
                        continue
                    self.DrawShape(file, self.canvas.layers[layer].drawnShapes[i].lines)
            self.MoveToolUp(file)
            self.MoveToHome(file)
            file.close()

    def TravelTo(self, file, position):
        self.MoveToolUp(file)
        self.MoveXY(file, position[0], position[1], 4)
        self.position = position

    def DrawShape(self, file, lines):
        for line in range(len(lines)):
            self.WriteMeriCodeLine(file, lines[line].x0, lines[line].y0, lines[line].x1, lines[line].y1)

    def DrawShapeReversed(self, file, lines):
        for line in reversed(lines):
            self.WriteMeriCodeLine(file, line.x0, line.y0, line.x1, line.y1)

    def WriteMeriCodeLine(self, file, x0, y0, x1, y1):
        if (abs(self.position[0] - x0) <= self.mergeDistance and abs(self.position[1] - y0) <= self.mergeDistance): #check if first point of line is equal with the current position
            #create line from start to end
            offset = [0, 0]
            if self.cutting:
                self.MoveToolUp(file)
                self.RotateTool(file, self.GetAngle(y0 - y1, x0 - x1), 4)
                offset = self.GetOffsetPosition(self.toolOffsetRadius, self.GetAngle(y0 - y1, x0 - x1))
                self.MoveToolDown(file)
            self.MoveXY(file, x1 + offset[0], y1 + offset[1], 4)
            return

        if (abs(self.position[0] - x1) <= self.mergeDistance and abs(self.position[1] - y1) <= self.mergeDistance): #check if the last point of the line is equal to the current position
            offset = [0, 0]
            if self.cutting:
                self.MoveToolUp(file)
                self.RotateTool(file, self.GetAngle(y1 - y0, x1 - x0), 4)
                offset = self.GetOffsetPosition(self.toolOffsetRadius, self.GetAngle(y1 - y0, x1 - x0))
                self.MoveToolDown(file)
            self.MoveXY(file, x0 + offset[0], y0 + offset[1], 4)
            return

        #if current position isn't equal to the start or end of the line then travel there
        offset = [0, 0]
        if self.cutting:
            self.MoveToolUp(file)
            self.RotateTool(file, self.GetAngle(y0 - y1, x0 - x1), 4)
            offset = self.GetOffsetPosition(self.toolOffsetRadius, self.GetAngle(y0 - y1, x0 - x1))
        self.TravelTo(file, [x0 + offset[0], y0 + offset[1]])
        self.MoveToolDown(file)
        self.MoveXY(file, x1 + offset[0], y1 + offset[1], 4)

    
    def MoveToolUp(self, file):
        file.write("<M0 Z" + str(10) + ">" + "\n")

    def MoveToolDown(self, file):
        file.write("<M0 Z" + str(0) + ">" + "\n")
    
    def MoveToHome(self, file):
        file.write("<M0 X0 Y0 T0>" + "\n") #move the tool in the material
        self.MoveToolDown(file)
    def MoveXY(self, file, x, y, ndigits):
        file.write("<M0 X" + str(round(x, ndigits)) + " Y" + str(round(y, ndigits)) + ">" + "\n")
        self.position = [x, y]

    def RotateTool(self, file, degrees, ndigits):
        file.write("<M0 T" + str(round(degrees, ndigits)) + ">" + "\n")

    @staticmethod
    def GetAngle(point0, point1):
        angle = math.degrees(math.atan2(point0, point1))
        if angle < 0:
            angle += 360
        return angle

    #this is for when the tool can rotate and the centerpoint of the tool changes based on its rotation
    @staticmethod
    def GetOffsetPosition(radius, angle):
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
