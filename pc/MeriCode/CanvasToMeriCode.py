import math
import os

import UI.CanvasShapes as CanvasShapes
from MeriCode.MericodeSlicingOptions import MericodeSlicingOptions
from MeriCode.ShortestPathCalculator import ShortestPathCalculator

class CanvasToMeriCode:
    def __init__(self, canvas, slicingOptions : MericodeSlicingOptions):
        self.centerToolPosition = [0, 0]
        self.rotation = 0
        self.canvas = canvas
        self.mergeDistance = 0.0001
        self.slicingOptions = slicingOptions
        self.cutting = slicingOptions.cutting
        self.toolOffsetRadius = -2
        self.numberOfCuts = 3
        self.currentCut = 0
        if not self.cutting:
            self.numberOfCuts = 1
        self.incresementPerCut = -6
        self.continueLineAngle = 4
        self.decimalRoundingMeriCode = 4

        self.travels = 0
        self.lines = 0
        self.shapes = 0
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)

        with open(os.path.dirname(dname) + '/Test/MeriCodeTestFile.txt', "w") as file:
            for cut in range(self.numberOfCuts):
                self.currentCut = cut

                for layer in range(len(self.canvas.layers)):
                    shapesToDraw = self.canvas.layers[layer].drawnShapes
                    if len(shapesToDraw) == 0:
                        continue
                    if self.slicingOptions.calculatePathOrder:
                        shapesToDraw = ShortestPathCalculator.CalculateShortestPath(self.canvas.layers[layer].drawnShapes)

                    for i in range(len(shapesToDraw)):
                        shapeEndPosition = shapesToDraw[i].GetEndPosition()
                        nextShapeEndPosition = [0, 0]
                        nextShapeStartPosition = [0, 0]

                        if len(shapesToDraw) - 1 != i:
                            nextShapeEndPosition = shapesToDraw[i + 1].GetEndPosition()
                            nextShapeStartPosition = shapesToDraw[i + 1].GetStartPosition()

                        if math.isclose(self.centerToolPosition[0], nextShapeEndPosition[0], rel_tol=self.mergeDistance) and math.isclose(self.centerToolPosition[1], nextShapeEndPosition[1], rel_tol=self.mergeDistance):
                            self.DrawShapeReversed(file, shapesToDraw[i].GetLinePositions(), nextShapeStartPosition)
                            continue
                        if math.isclose(self.centerToolPosition[0], nextShapeStartPosition[0], rel_tol=self.mergeDistance) and math.isclose(self.centerToolPosition[1], nextShapeStartPosition[1], rel_tol=self.mergeDistance):
                            self.DrawShape(file, shapesToDraw[i].GetLinePositions(), nextShapeStartPosition)
                            continue

                        self.DrawShapeReversed(file, shapesToDraw[i].GetLinePositions(), nextShapeStartPosition)

            self.currentCut = 0
            self.MoveToolUp(file)
            self.MoveToHome(file)

            file.close()

    def DrawShape(self, file, lines, possibleNextPoint):
        self.shapes += 1
        for line in range(len(lines)):
            nextLine = possibleNextPoint

            if line != len(lines) - 1:
                nextLine = [lines[line + 1].x0, lines[line + 1].y0]

            self.CreateMeriCodeLine(file, [lines[line].x0, lines[line].y0], [lines[line].x1, lines[line].y1], nextLine)

    def DrawShapeReversed(self, file, lines, possibleNextPoint):
        self.shapes += 1
        for line in reversed(range(len(lines))):
            nextLine = possibleNextPoint

            if line != 0:
                nextLine = [lines[line - 1].x0, lines[line - 1].y0]

            self.CreateMeriCodeLine(file, [lines[line].x1, lines[line].y1], [lines[line].x0, lines[line].y0], nextLine)
    
    def CreateMeriCodeLine(self, file, lineStart, lineEnd, possibleNextPoint):
        self.lines += 1

        if possibleNextPoint[0] == lineStart[0] and possibleNextPoint[1] == lineStart[1]:
            tmpLine = lineStart
            lineStart = lineEnd
            lineEnd = tmpLine

        if self.cutting:
            self.MoveToolUp(file)
            angle = self.GetAngle(lineStart[1] - lineEnd[1], lineStart[0] - lineEnd[0])
            self.MoveXYT(file, lineStart[0], lineStart[1], angle)
            self.MoveToolDown(file)
            self.MoveXYT(file, lineEnd[0], lineEnd[1], angle)
            return

        if ((math.isclose(lineStart[0], self.centerToolPosition[0], rel_tol=self.mergeDistance)) and (math.isclose(lineStart[1], self.centerToolPosition[1], rel_tol=self.mergeDistance))):            
            pass
        else:
            self.TravelTo(file, [lineStart[0], lineStart[1]])

        self.MoveToolDown(file)
        self.MoveXY(file, lineEnd[0], lineEnd[1])

    
#################### Functions to help write mericode

    def MoveToolUp(self, file):
        self.travels += 1
        file.write("<M0 Z" + str(20) + ">" + "\n")

    def MoveToolDown(self, file):
        file.write("<M0 Z" + str(0 + (self.currentCut * self.incresementPerCut)) + ">" + "\n")
    
    def MoveToHome(self, file):
        file.write("<M0 X0 Y0 T0>" + "\n")
        self.MoveToolDown(file)

    #use this if the center point always stays the same eg. using a pen
    def MoveXY(self, file, x, y):
        file.write("<M0 X" + str(round(x, self.decimalRoundingMeriCode)) + " Y" + str(round(y, self.decimalRoundingMeriCode)) + ">" + "\n")
        self.centerToolPosition = [x, y]

    #DO NOT USE WITH NON ROTATING TOOLS!!!
    #use this for tools that need to rotate eg. using a knife tip. the x and y position is the contact position
    def MoveXYT(self, file, x, y, t): 
        self.centerToolPosition = [x, y]
        self.rotation = round(t, self.decimalRoundingMeriCode)
        offset = self.GetOffsetPosition(self.toolOffsetRadius, self.rotation)
        x -= offset[0]
        y -= offset[1]
        file.write("<M0 X" + str(round(x, self.decimalRoundingMeriCode)) + " Y" + str(round(y, self.decimalRoundingMeriCode)) + " T" + str(round(t, self.decimalRoundingMeriCode)) + ">" + "\n")

    def TravelXY(self, file, x, y):
        file.write("<M1 X" + str(round(x, self.decimalRoundingMeriCode)) + " Y" + str(round(y, self.decimalRoundingMeriCode)) + ">" + "\n")
        self.centerToolPosition = [x, y]

    def RotateTool(self, file, degrees):
        file.write("<M0 T" + str(round(degrees, self.decimalRoundingMeriCode)) + ">" + "\n")
        self.rotation = round(degrees, self.decimalRoundingMeriCode)

    def TravelTo(self, file, centerToolPosition):
        self.MoveToolUp(file)
        self.TravelXY(file, centerToolPosition[0], centerToolPosition[1])
        self.centerToolPosition = centerToolPosition

################## methods for calculating angle and offset for the cutting knife 
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
