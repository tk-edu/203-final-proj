import pygame as pyg

import color

class Text:
    def __init__(self, text, font, font_size, color, antialias):
        self.text = text
        self.font = pyg.font.SysFont(font, font_size)
        self.surface = self.font.render(text, False, color)
        self.color = color
        self.__color_offset = 0
        self.__color_reversing = False
        self.antialias = antialias
    def update(self, text = None, color = None):
        self.text = text if text else self.text
        self.color = color if color else self.color
        self.surface = self.font.render(self.text, self.antialias, self.color)
    # Result = (color2 - color1) * fraction + color1
    def flash_colors(self, color_1, color_2, speed):
        if self.__color_offset >= 1000:
            self.color = color_2
            self.__color_reversing = True
        elif self.__color_offset <= 0:
            self.color = color_1
            self.__color_reversing = False
        self.__color_offset += -speed if self.__color_reversing else speed
        # print(f'{self.__color_offset}')
        self.update()