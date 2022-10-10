from UI.Colors import Colors

def DrawGrid(canvas, cellSize, edges = False):
    for i in range(int(canvas.winfo_reqwidth() / cellSize)):
        if not i or i is int(canvas.winfo_reqwidth() / cellSize) and not edges: continue
        canvas.create_line((i * cellSize), 0, (i * cellSize), canvas.winfo_reqheight(), fill=Colors.GRIDCOLOR, width=1)
    for i in range(int(canvas.winfo_reqheight() / cellSize)):
        if not i or i is int(canvas.winfo_reqheight() / cellSize) and not edges: continue
        canvas.create_line(0, (i * cellSize), canvas.winfo_reqwidth(), (i * cellSize), fill=Colors.GRIDCOLOR, width=1)
    return canvas

def DrawCircle(canvas, x, y, radius):
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=Colors.COLISIONCIRCLECOLOR, width=2)
