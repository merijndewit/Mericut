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
        self.canvas.parent.DrawLine(self.xOffset, 0 + self.yOffset, self.xOffset, self.canvas.parent.GetHeight() + self.yOffset, color)
        self.canvas.parent.DrawLine(0 + self.xOffset, 0 + self.yOffset, self.canvas.parent.GetWidth() + self.xOffset, 0 + self.yOffset, color)

        offsetX = self.xOffset % self.cellSize - self.cellSize
        offsetY = self.yOffset % self.cellSize - self.cellSize
        for i in range(int(self.canvas.parent.GetWidth() / self.cellSize) + 1):
            self.canvas.parent.DrawLine((i * self.cellSize) + offsetX, 0 + offsetY, (i * self.cellSize) + offsetX, self.canvas.parent.GetHeight() + offsetY, color)
        for i in range(int(self.canvas.parent.GetHeight() / self.cellSize) + 1):
            self.canvas.parent.DrawLine(0 + offsetX, (i * self.cellSize) + offsetY, self.canvas.parent.GetWidth() + offsetX, (i * self.cellSize) + offsetY, color)

    def ReDraw(self, cellSize, xOffset, yOffset):
        self.cellSize = cellSize
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.DrawGrid()