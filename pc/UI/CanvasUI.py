from UI.Colors import Colors

class CanvasGrid():
    def __init__(self, canvas, cellSize, xOffset, yOffset):
        self.canvasLines = []
        self.cellSize = cellSize
        self.canvas = canvas
        self.xOffset = (xOffset % self.cellSize) - 10
        self.yOffset = (yOffset % self.cellSize) - 10
        self.DrawGrid()

    def DrawGrid(self, color=Colors.GRIDCOLOR):
        self.canvasLines.append(self.canvas.create_line(self.xOffset, 0 + self.yOffset, self.xOffset, self.canvas.winfo_reqheight() + self.yOffset, fill=color, width=2))
        self.canvasLines.append(self.canvas.create_line(0 + self.xOffset, 0 + self.yOffset, self.canvas.winfo_reqwidth() + self.xOffset, 0 + self.yOffset, fill=color, width=2))

        offsetX = self.xOffset % self.cellSize - self.cellSize
        offsetY = self.yOffset % self.cellSize - self.cellSize
        for i in range(int(self.canvas.winfo_reqwidth() / self.cellSize) + 1):
            self.canvasLines.append(self.canvas.create_line((i * self.cellSize) + offsetX, 0 + offsetY, (i * self.cellSize) + offsetX, self.canvas.winfo_reqheight() + offsetY, fill=color, width=1))
        for i in range(int(self.canvas.winfo_reqheight() / self.cellSize) + 1):
            self.canvasLines.append(self.canvas.create_line(0 + offsetX, (i * self.cellSize) + offsetY, self.canvas.winfo_reqwidth() + offsetX, (i * self.cellSize) + offsetY, fill=color, width=1))

    def DeleteGrid(self):
        for i in range(len(self.canvasLines)):
            self.canvas.delete(self.canvasLines[i])

    def ReDraw(self, cellSize, xOffset, yOffset):
        self.cellSize = cellSize
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.DeleteGrid()
        self.DrawGrid()