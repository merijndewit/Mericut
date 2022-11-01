from UI.Colors import Colors

def DrawGrid(canvas, cellSize, color=Colors.GRIDCOLOR):
    canvasLines = []
    for i in range(int(canvas.winfo_reqwidth() / cellSize) + 1):
        canvasLines.append(canvas.create_line((i * cellSize), 0, (i * cellSize), canvas.winfo_reqheight(), fill=color, width=1))
    for i in range(int(canvas.winfo_reqheight() / cellSize) + 1):
        canvasLines.append(canvas.create_line(0, (i * cellSize), canvas.winfo_reqwidth(), (i * cellSize), fill=color, width=1))
    return canvasLines

class CanvasGridScale():
    def __init__(self, canvas, pixelsPerMM):
        self.canvas = canvas
        self.pixelsPerMM = pixelsPerMM
        self.Update()

    def Update(self):
        self.position = [self.canvas.winfo_reqwidth() - 40, self.canvas.winfo_reqheight() - 40]
        self.text = self.canvas.create_text(self.position[0], self.position[1], fill="#000000", text=str(self.pixelsPerMM)+"mm")


