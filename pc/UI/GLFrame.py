from OpenGL import GL
from pyopengltk import OpenGLFrame

import tkinter as tk
from OpenGL.GL import *

class GLFrame(OpenGLFrame):
    def __init__(self, parent, *args, **kw):
        super().__init__(*args, **kw)
        self.parent = parent
        self.configure( width=590,
                        height=590,
                        highlightthickness=0)
        self.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), rowspan=4, sticky=tk.NSEW)
        
        self.lines = []
        self.lineColors = []
        self.addLine([100, 100, 400, 400], [0.3, 0.1, 0.3])
        self.addLine([50, 200, 400, 300], [0.3, 0.1, 0.3])

    def initgl(self):
        glViewport(0, 0, self.width, self.height)
        glClearColor(1.0,1.0,1.0,0.0)

        # setup projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)

        # setup identity model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        
    def redraw(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        for i in range(len(self.lines)):
            glBegin(GL_LINES)

            glColor3f(self.lineColors[i][0], self.lineColors[i][1], self.lineColors[i][2])

            glVertex2f(self.lines[i][0],self.lines[i][1])
            glVertex2f(self.lines[i][2],self.lines[i][3])
            glEnd()

        glFlush()

    def addLine(self, line : tuple, color : tuple):
        self.lines.append(line)  #line = [x, y, x1, y1]
        self.lineColors.append(color) #color = [r, g, b]

    

if __name__=='__main__':

    root = tk.Tk()
    app = GLFrame(root, None, width=500,height=500)
    app.pack(fill=tk.BOTH, expand=tk.YES)
    app.mainloop()