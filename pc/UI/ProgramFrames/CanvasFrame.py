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
        self.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), rowspan=4, sticky=tkinter.NSEW)

        #pygame window
        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.pygame = pygame
        self.pygame.display.init()
        self.screen = pygame.display.set_mode((500,500), vsync=1)
        self.canvas = DrawingCanvas(self)


    def UpdateCanvas(self):
        #input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEWHEEL:
                self.canvas.Scroll(event.y)
            if pygame.mouse.get_focused():
                #cursor
                cursor = pygame.mouse.get_pos()
                self.canvas.Motion(cursor[0], cursor[1])
                #mouse buttons
                buttons = pygame.mouse.get_pressed() #button1, button2, button3
                if buttons[0]:
                    self.canvas.Clicked(cursor[0], cursor[1])
                else:
                    self.canvas.Released()
                


        self.pygame.display.update()
        
    def Clear(self):
        self.screen.fill((255,255,255))
        print("clear")

    def InitializeDisplay(self):
        self.screen.fill((255,255,255))
        self.pygame.display.update()

    @staticmethod
    def ConvertHexToRGB(hexColor):
        hexColor = hexColor.lstrip('#')
        return tuple(int(hexColor[i:i+2], 16) for i in (0, 2, 4))

    def DrawLine(self, x0, y0, x1, y1, hexColor):
        self.pygame.draw.line(self.screen, start_pos=(x0, y0), end_pos=(x1, y1), color=self.ConvertHexToRGB(hexColor))

    def DrawCircle(self, x, y, radius, hexColor):
        self.pygame.draw.circle(self.screen, center=(x, y), radius=radius, color=self.ConvertHexToRGB(hexColor))

    def GetHeight(self):
        return self.screen.get_height()
    
    def GetWidth(self):
        return self.screen.get_width()