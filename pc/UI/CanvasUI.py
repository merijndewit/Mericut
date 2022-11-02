from UI.Colors import Colors

class CanvasGrid():
    def __init__(self, canvas, cellSize):
        self.canvasLines = []
        self.cellSize = cellSize
        self.canvas = canvas
        self.DrawGrid()

    def DrawGrid(self, color=Colors.GRIDCOLOR):
        for i in range(int(self.canvas.winfo_reqwidth() / self.cellSize) + 1):
            self.canvasLines.append(self.canvas.create_line((i * self.cellSize), 0, (i * self.cellSize), self.canvas.winfo_reqheight(), fill=color, width=1))
        for i in range(int(self.canvas.winfo_reqheight() / self.cellSize) + 1):
            self.canvasLines.append(self.canvas.create_line(0, (i * self.cellSize), self.canvas.winfo_reqwidth(), (i * self.cellSize), fill=color, width=1))

    def DeleteGrid(self):
        for i in range(len(self.canvasLines)):
            self.canvas.delete(self.canvasLines[i])

    def ReDraw(self, cellSize):
        self.cellSize = cellSize
        self.DeleteGrid()
        self.DrawGrid()
