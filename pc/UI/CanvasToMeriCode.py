class CanvasToMeriCode:
    def __init__(self, canvas):
        self.position = [0, 0]
        self.canvas = canvas
        self.mergeDistance = 0.04
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
                    self.MoveTo(file, shapeStartPosition)
                    self.DrawShape(file, self.canvas.layers[layer].drawnShapes[i].lines)
            self.MoveToolUp(file)
            self.MoveToHome(file)
            file.close()

    def MoveTo(self, file, position):
        self.MoveToolUp(file)
        file.write("<M0 X" + str(round(position[0], 4)) + " Y" + str(round(position[1], 4)) + ">" + "\n")
        self.position = position
        self.MoveToolDown(file)

    def DrawShape(self, file, lines):
        for line in range(len(lines)):
            self.WriteMeriCodeLine(file, lines[line].x0, lines[line].y0, lines[line].x1, lines[line].y1)

    def DrawShapeReversed(self, file, lines):
        for line in reversed(lines):
            self.WriteMeriCodeLine(file, line.x0, line.y0, line.x1, line.y1)

    def WriteMeriCodeLine(self, file, x0, y0, x1, y1):
        if (abs(self.position[0] - x0) <= self.mergeDistance and abs(self.position[1] - y0) <= self.mergeDistance):
            file.write("<M0 X" + str(round(x1, 4)) + " Y" + str(round(y1, 4)) + ">" + "\n") #move the tool to the start of the line
            self.position = [x1, y1]
            return
        if (abs(self.position[0] - x1) <= self.mergeDistance and abs(self.position[1] - y1) <= self.mergeDistance):
            file.write("<M0 X" + str(round(x0, 4)) + " Y" + str(round(y0, 4)) + ">" + "\n") #move the tool to the start of the line
            self.position = [x0, y0]
            return
        self.MoveToolUp(file)
        file.write("<M0 X" + str(round(x0, 4)) + " Y" + str(round(y0, 4)) + ">" + "\n") #move the tool to the start of the line
        self.MoveToolDown(file)
        file.write("<M0 X" + str(round(x1, 4)) + " Y" + str(round(y1, 4)) + ">" + "\n") #move the tool to the start of the line
        self.position = [x1, y1]
    @staticmethod
    def MoveToolUp(file):
        file.write("<M0 Z" + str(20) + ">" + "\n")
    @staticmethod
    def MoveToolDown(file):
        file.write("<M0 Z" + str(0) + ">" + "\n")
    @staticmethod
    def MoveToHome(file):
        file.write("<M0 X0 Y0>" + "\n") #move the tool in the material
        CanvasToMeriCode.MoveToolDown(file)
