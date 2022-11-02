class CanvasToMeriCode:
    def __init__(self, canvas):
        self.position = [0, 0]
        self.canvas = canvas
        self.mergeDistance = 0.01
        with open('Test/MeriCodeTestFile.txt', "w") as file:
            file.write("<S1>" + "\n") #file start command
            for i in range(len(self.canvas.drawnShapes)):
                for line in range(len(self.canvas.drawnShapes[i].lines)):
                    #for now there are only lines
                    self.WriteMeriCodeLine(file, self.canvas.drawnShapes[i].lines[line].x0, self.canvas.drawnShapes[i].lines[line].y0, self.canvas.drawnShapes[i].lines[line].x1, self.canvas.drawnShapes[i].lines[line].y1)

            self.MoveToolUp(file)
            self.MoveToHome(file)
            file.write("<S0>" + "\n") #file stop command
            file.close()

    def WriteMeriCodeLine(self, file, x0, y0, x1, y1):
        if (abs(self.position[0] - x0) <= self.mergeDistance and abs(self.position[1] - y0) <= self.mergeDistance):
            file.write("<M0 X" + str(x1) + " Y" + str(y1) + ">" + "\n") #move the tool to the start of the line
            self.position = [x1, y1]
            return
        self.MoveToolUp(file)
        file.write("<M0 X" + str(x0) + " Y" + str(y0) + ">" + "\n") #move the tool to the start of the line
        self.MoveToolDown(file)
        file.write("<M0 X" + str(x1) + " Y" + str(y1) + ">" + "\n") #move the tool to the start of the line
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
