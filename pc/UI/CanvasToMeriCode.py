class CanvasToMeriCode:
    def __init__(self, canvas):
        self.position = [0, 0]
        self.canvas = canvas
        self.mergeDistance = 0.01
        with open('Test/MeriCodeTestFile.txt', "w") as file:
            file.write("<S1>" + "\n") #file start command
            for i in range(len(self.canvas.drawnShapes)):
                self.WriteShape(file, self.canvas.drawnShapes[i].lines)

            self.MoveToolUp(file)
            self.MoveToHome(file)
            file.write("<S0>" + "\n") #file stop command
            file.close()

    def WriteShape(self, file, lines):
        for i in range(len(lines)):
            if (i == len(lines) - 1):
                if (self.canvas.drawnShapes[i + 1] is None):
                    return
                        
                return 
            self.WriteMeriCodeLine(file, lines[i].x0, lines[i].y0, lines[i].x1, lines[i].y1)


    def WriteMeriCodeLine(self, file, x0, y0, x1, y1):
        if (abs(self.position[0] - x0) <= self.mergeDistance and abs(self.position[1] - y0) <= self.mergeDistance):
            file.write("<M0 X" + str(x1) + " Y" + str(y1) + ">" + "\n") #move the tool to the start of the line
            self.position = [x1, y1]
            return
        if (abs(self.position[0] - x1) <= self.mergeDistance and abs(self.position[1] - y1) <= self.mergeDistance):
            file.write("<M0 X" + str(x0) + " Y" + str(y0) + ">" + "\n") #move the tool to the start of the line
            self.position = [x0, y0]
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
