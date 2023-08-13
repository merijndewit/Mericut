import math
import UI.CanvasShapes as CanvasShapes
class CanvasToMeriCode:
    def __init__(self, canvas, cutting):
        self.position = [0, 0]
        self.rotation = 0
        self.canvas = canvas
        self.mergeDistance = 0.05
        self.cutting = cutting
        self.toolOffsetRadius = 3.75
        self.numberOfCuts = 1
        self.currentCut = 0
        if not self.cutting:
            self.numberOfCuts = 1
        self.incresementPerCut = -3
        self.continueLineAngle = 4

        self.travels = 0
        self.lines = 0
        self.shapes = 0

        with open('Test/MeriCodeTestFile.txt', "w") as file:
            for cut in range(self.numberOfCuts):
                self.currentCut = cut
                for layer in range(len(self.canvas.layers)):
                    for i in range(len(self.canvas.layers[layer].drawnShapes)):
                        shapeStartPosition = self.canvas.layers[layer].drawnShapes[i].GetStartPosition()
                        shapeEndPosition = self.canvas.layers[layer].drawnShapes[i].GetEndPosition()
                        offset = [0, 0]
                        if self.cutting:
                            offset = self.GetOffsetPosition(self.toolOffsetRadius, self.rotation)
                        if (abs((self.position[0] - offset[0]) - shapeStartPosition[0]) <= self.mergeDistance and abs((self.position[1] - offset[1])  - shapeStartPosition[1]) <= self.mergeDistance):
                            self.DrawShapeReversed(file, self.canvas.layers[layer].drawnShapes[i].lines)
                            continue
                        if (abs((self.position[0] - offset[0]) - shapeEndPosition[0]) <= self.mergeDistance and abs((self.position[1] - offset[1]) - shapeEndPosition[1]) <= self.mergeDistance):
                            self.DrawShape(file, self.canvas.layers[layer].drawnShapes[i].lines)
                            continue
                        self.DrawShape(file, self.canvas.layers[layer].drawnShapes[i].lines)
            self.currentCut = 0
            self.MoveToolUp(file)
            self.MoveToHome(file)

            file.close()

    def TravelTo(self, file, position):
        self.MoveToolUp(file)
        self.TravelXY(file, position[0], position[1], 4)
        self.position = position

    def DrawShape(self, file, lines):
        self.shapes += 1
        for line in range(len(lines)):
            self.WriteMeriCodeLine(file, self.canvas.CanvasPosXToNormalPosX(lines[line].x0), self.canvas.CanvasPosYToNormalPosY(lines[line].y0), self.canvas.CanvasPosXToNormalPosX(lines[line].x1), self.canvas.CanvasPosYToNormalPosY(lines[line].y1))

    def DrawShapeReversed(self, file, lines):
        self.shapes += 1
        for line in reversed(lines):
            self.WriteMeriCodeLine(file, self.canvas.CanvasPosXToNormalPosX(line.x0), self.canvas.CanvasPosYToNormalPosY(line.y0), self.canvas.CanvasPosXToNormalPosX(line.x1), self.canvas.CanvasPosYToNormalPosY(line.y1))

    def WriteMeriCodeLine(self, file, x0, y0, x1, y1):
        self.lines += 1
        offsetTool = [0, 0]
        if self.cutting:
            offsetTool = self.GetOffsetPosition(self.toolOffsetRadius, self.rotation)
        if (abs((self.position[0] - offsetTool[0]) - x0) <= self.mergeDistance and abs((self.position[1] - offsetTool[1]) - y0) <= self.mergeDistance): #check if first point of line is equal with the current position
            #create line from start to end
            offset = [0, 0]
            if self.cutting:
                angle = self.GetAngle(y0 - y1, x0 - x1)
                moveToolDown = False
                if abs(self.rotation - angle) > self.continueLineAngle:
                    self.MoveToolUp(file)
                    moveToolDown = True
                offset = self.GetOffsetPosition(self.toolOffsetRadius, self.GetAngle(y0 - y1, x0 - x1))
                oldOffset = self.GetOffsetPosition(self.toolOffsetRadius, self.rotation)
                self.MoveXYT(file, (self.position[0] - oldOffset[0]) + offset[0], (self.position[1] - oldOffset[1]) + offset[1], self.GetAngle(y0 - y1, x0 - x1), 4)
                if moveToolDown:
                    self.MoveToolDown(file)
            self.MoveXY(file, x1 + offset[0], y1 + offset[1], 4)
            return

        if (abs((self.position[0] - offsetTool[0]) - x1) <= self.mergeDistance and abs((self.position[1] - offsetTool[1]) - y1) <= self.mergeDistance): #check if the last point of the line is equal to the current position
            offset = [0, 0]
            if self.cutting:
                angle = self.GetAngle(y1 - y0, x1 - x0)
                moveToolDown = False
                if abs(self.rotation - angle) > self.continueLineAngle:
                    self.MoveToolUp(file)
                    moveToolDown = True
                offset = self.GetOffsetPosition(self.toolOffsetRadius, self.GetAngle(y1 - y0, x1 - x0))
                oldOffset = self.GetOffsetPosition(self.toolOffsetRadius, self.rotation)
                self.MoveXYT(file, (self.position[0] - oldOffset[0]) + offset[0], (self.position[1] - oldOffset[1]) + offset[1], self.GetAngle(y1 - y0, x1 - x0), 4)
                if moveToolDown:
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
        self.travels += 1
        file.write("<M0 Z" + str(20) + ">" + "\n")

    def MoveToolDown(self, file):
        file.write("<M0 Z" + str(0 + (self.currentCut * self.incresementPerCut)) + ">" + "\n")
    
    def MoveToHome(self, file):
        file.write("<M0 X0 Y0 T0>" + "\n")
        self.MoveToolDown(file)

    def MoveXY(self, file, x, y, ndigits):
        file.write("<M0 X" + str(round(x, ndigits)) + " Y" + str(round(y, ndigits)) + ">" + "\n")
        self.position = [x, y]

    def MoveXYT(self, file, x, y, t, ndigits):
        file.write("<M0 X" + str(round(x, ndigits)) + " Y" + str(round(y, ndigits)) + " T" + str(round(t, ndigits)) + ">" + "\n")
        self.position = [x, y]
        self.rotation = round(t, ndigits)

    def TravelXY(self, file, x, y, ndigits):
        file.write("<M1 X" + str(round(x, ndigits)) + " Y" + str(round(y, ndigits)) + ">" + "\n")
        self.position = [x, y]

    def RotateTool(self, file, degrees, ndigits):
        file.write("<M0 T" + str(round(degrees, ndigits)) + ">" + "\n")
        self.rotation = round(degrees, ndigits)

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
