import math
import os

import UI.CanvasShapes as CanvasShapes
from MeriCode.MericodeSlicingOptions import MericodeSlicingOptions
class CanvasToMeriCode:
    def __init__(self, canvas, slicingOptions : MericodeSlicingOptions):
        self.position = [0, 0]
        self.rotation = 0
        self.canvas = canvas
        self.mergeDistance = 0.01
        self.slicingOptions = slicingOptions
        self.cutting = slicingOptions.cutting
        self.toolOffsetRadius = 2
        self.numberOfCuts = 1
        self.currentCut = 0
        if not self.cutting:
            self.numberOfCuts = 1
        self.incresementPerCut = -3
        self.continueLineAngle = 4

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
                    if self.slicingOptions.calculatePathOrder:
                        shapesToDraw = self.CalculateNewPathOrder(self.canvas.layers[layer].drawnShapes)

                    for i in range(len(shapesToDraw)):
                        shapeEndPosition = shapesToDraw[i].GetEndPosition()
                        nextShapeEndPosition = [0, 0]
                        nextShapeStartPosition = [0, 0]

                        if len(shapesToDraw) - 1 != i:
                            nextShapeEndPosition = shapesToDraw[i + 1].GetEndPosition()
                            nextShapeStartPosition = shapesToDraw[i + 1].GetStartPosition()

                        offset = [0, 0]
                        if self.cutting:
                            offset = self.GetOffsetPosition(self.toolOffsetRadius, self.rotation)

                        if (abs(self.position[0] - nextShapeEndPosition[0]) <= self.mergeDistance and abs(self.position[1] - nextShapeEndPosition[1]) <= self.mergeDistance):
                            self.DrawShapeReversed(file, shapesToDraw[i].lines, nextShapeStartPosition)
                            continue
                        if (abs(self.position[0] - nextShapeStartPosition[0]) <= self.mergeDistance and abs(self.position[1] - nextShapeStartPosition[1]) <= self.mergeDistance):
                            self.DrawShape(file, shapesToDraw[i].lines, nextShapeStartPosition)
                            continue

                        self.DrawShapeReversed(file, shapesToDraw[i].lines, nextShapeStartPosition)


            self.currentCut = 0
            self.MoveToolUp(file)
            self.MoveToHome(file)

            file.close()

    def CalculateNewPathOrder(self, shapes):
        newShapeOrder = []
        visitedShapesIndex = []
        currentPosition = None

        def CheckForSamePosition(currentPosition):
            for i in range(len(shapes)):
                if i in visitedShapesIndex:
                    continue

                shapeStartPosition = shapes[i].GetStartPosition()
                shapeEndPosition = shapes[i].GetEndPosition()
                maxMergeDistance = 2
                if math.isclose(shapeStartPosition[0], currentPosition[0], rel_tol=maxMergeDistance) and math.isclose(shapeStartPosition[1], currentPosition[1], rel_tol=maxMergeDistance):

                    currentPosition = shapes[i].GetEndPosition()
                    visitedShapesIndex.append(i)
                    newShapeOrder.append(shapes[i])
                    continue
                elif math.isclose(shapeEndPosition[0], currentPosition[0], rel_tol=maxMergeDistance) and math.isclose(shapeEndPosition[1], currentPosition[1], rel_tol=maxMergeDistance):

                    currentPosition = shapes[i].GetStartPosition()
                    visitedShapesIndex.append(i)
                    newShapeOrder.append(shapes[i])
                    continue

            else: #coudn't find shape that starts or ends on current position 
                for i in range(len(shapes)):
                    if not i in visitedShapesIndex:
                        currentPosition = shapes[i].GetEndPosition()
                        visitedShapesIndex.append(i)
                        newShapeOrder.append(shapes[i])
                        break

        currentPosition = shapes[0].GetStartPosition()
        visitedShapesIndex.append(0)
        newShapeOrder.append(shapes[0])

        while len(shapes) != len(visitedShapesIndex):
            CheckForSamePosition(currentPosition)

        return newShapeOrder

    def TravelTo(self, file, position):
        self.MoveToolUp(file)
        self.TravelXY(file, position[0], position[1], 4)
        self.position = position

    def DrawShape(self, file, lines, possibleNextPoint):
        self.shapes += 1
        for line in range(len(lines)):
            nextLine = possibleNextPoint

            if line != len(lines) - 1:
                nextLine = [self.canvas.CanvasPosXToNormalPosX(lines[line + 1].x0), self.canvas.CanvasPosYToNormalPosY(lines[line + 1].y0)]

            self.WriteMeriCodeLine(file, [self.canvas.CanvasPosXToNormalPosX(lines[line].x0), self.canvas.CanvasPosYToNormalPosY(lines[line].y0)], [self.canvas.CanvasPosXToNormalPosX(lines[line].x1), self.canvas.CanvasPosYToNormalPosY(lines[line].y1)], nextLine)

    def DrawShapeReversed(self, file, lines, possibleNextPoint):
        self.shapes += 1
        for line in reversed(range(len(lines))):
            nextLine = possibleNextPoint

            if line != 0:
                nextLine = [self.canvas.CanvasPosXToNormalPosX(lines[line - 1].x0), self.canvas.CanvasPosYToNormalPosY(lines[line - 1].y0)]

            if(self.cutting):
                self.CutMeriCodeLine(file, [self.canvas.CanvasPosXToNormalPosX(lines[line].x1), self.canvas.CanvasPosYToNormalPosY(lines[line].y1)], [self.canvas.CanvasPosXToNormalPosX(lines[line].x0), self.canvas.CanvasPosYToNormalPosY(lines[line].y0)], nextLine)
                continue

            self.DrawMeriCodeLine(file, [self.canvas.CanvasPosXToNormalPosX(lines[line].x1), self.canvas.CanvasPosYToNormalPosY(lines[line].y1)], [self.canvas.CanvasPosXToNormalPosX(lines[line].x0), self.canvas.CanvasPosYToNormalPosY(lines[line].y0)], nextLine)
    
    #this code bassicly does the same as cutting a line. but i found that having both functionalities in the same function is quite confusing, thats why they are seperate
    def DrawMeriCodeLine(self, file, lineStart, lineEnd, possibleNextPoint):
        self.lines += 1

        if possibleNextPoint[0] == lineStart[0] and possibleNextPoint[1] == lineStart[1]:
            tmpLine = lineStart
            lineStart = lineEnd
            lineEnd = tmpLine

        if abs(lineStart[0] - self.position[0]) >= self.mergeDistance and abs(lineStart[1] - self.position[1]) >= self.mergeDistance:
            self.TravelTo(file, [lineStart[0], lineStart[1]])

        self.MoveToolDown(file)
        self.MoveXY(file, lineEnd[0], lineEnd[1], 4)

    def CutMeriCodeLine(self, file, lineStart, lineEnd, possibleNextPoint):
            self.lines += 1

            if possibleNextPoint[0] == lineStart[0] and possibleNextPoint[1] == lineStart[1]:
                tmpLine = lineStart
                lineStart = lineEnd
                lineEnd = tmpLine

            offset = [0, 0]

            angle = self.GetAngle(lineStart[1] - lineEnd[1], lineStart[0] - lineEnd[0])
            moveToolDown = False
            if abs(self.rotation - angle) > self.continueLineAngle:
                moveToolDown = True
                
            self.MoveToolUp(file)
            offset = self.GetOffsetPosition(self.toolOffsetRadius, angle)
            oldOffset = self.GetOffsetPosition(self.toolOffsetRadius, self.rotation)
            self.MoveXYT(file, (self.position[0] - oldOffset[0]) + offset[0], (self.position[1] - oldOffset[1]) + offset[1], angle, 4)
            if moveToolDown:
                self.MoveToolDown(file)
            self.MoveXY(file, lineEnd[0] + offset[0], lineEnd[1] + offset[1], 4)

    
#################### Functions to help write mericode

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
