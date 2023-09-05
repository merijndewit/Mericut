import customtkinter
import tkinter
import os
import pygame
import time

from UI.Colors import Colors
from UI.DrawingCanvas import DrawingCanvas


class HardwareAcceleratedCanvas(tkinter.Canvas):
    def __init__(self, parent, frameParent, *args, **kwargs):
        tkinter.Canvas.__init__(self, frameParent, *args, **kwargs)
        self.parent = parent
        self.configure( width=600,
                        height=600)
        self.canvas = DrawingCanvas(self)
        self.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), rowspan=4, sticky=tkinter.NSEW)

        #pygame window
        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.pygame = pygame
        self.pygame.display.init()
        self.screen = pygame.display.set_mode((500,500), vsync=1)
        time.sleep(2)


    def InitializeDisplay(self):
        self.screen.fill((255,255,255))

        self.DrawLine(0, 100, 100, 300)
        self.pygame.display.update()

    def DrawLine(self, x0, y0, x1, y1):
        self.pygame.draw.line(self.screen, start_pos=(x0, y0), end_pos=(x1, y1), color=(50, 50, 50))
        #print("draw line")
