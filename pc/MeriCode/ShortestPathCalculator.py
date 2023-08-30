import math

class ShortestPathCalculator:
    @staticmethod
    def CalculateShortestPath(shapes):
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

            else: #coudn't find shape that starts or ends on current centerToolPosition 
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