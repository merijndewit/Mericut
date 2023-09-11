from UI.Colors import Colors

class CanvasGrid():
    def __init__(self, drawingCanvas, cellSize, xOffset, yOffset):
        self.canvasLines = []
        self.cellSize = cellSize
        self.drawingCanvas = drawingCanvas
        self.xOffset = (xOffset % self.cellSize) - 10
        self.yOffset = (yOffset % self.cellSize) - 10
        #self.DrawGrid()

    def DrawGrid(self, color=Colors.GRIDCOLOR):
        self.drawingCanvas.DrawLine(self.xOffset, 0 + self.yOffset, self.xOffset, self.drawingCanvas.GetHeight() + self.yOffset, color)
        self.drawingCanvas.DrawLine(0 + self.xOffset, 0 + self.yOffset, self.drawingCanvas.GetWidth() + self.xOffset, 0 + self.yOffset, color)

        offsetX = self.xOffset % self.cellSize - self.cellSize
        offsetY = self.yOffset % self.cellSize - self.cellSize
        for i in range(int(self.drawingCanvas.GetWidth() / self.cellSize) + 1):
            self.drawingCanvas.DrawLine((i * self.cellSize) + offsetX, 0 + offsetY, (i * self.cellSize) + offsetX, self.drawingCanvas.GetHeight() + offsetY, color)
        for i in range(int(self.drawingCanvas.GetHeight() / self.cellSize) + 1):
            self.drawingCanvas.DrawLine(0 + offsetX, (i * self.cellSize) + offsetY, self.drawingCanvas.GetWidth() + offsetX, (i * self.cellSize) + offsetY, color)

    def ReDraw(self, cellSize, xOffset, yOffset):
        self.cellSize = cellSize
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.DrawGrid()