# https://pygame.readthedocs.io/en/latest/tiles/tiles.html
import pygame as pyg

from common import *

class Tileset:
    def __init__(self, file: str, tile_size: int, scale: int):
        self.file = file
        self.scale = scale
        self.tile_size = tile_size
        self.tiles = []

        self.image = pyg.image.load(f'assets/{self.file}').convert()
        self.image.set_colorkey((255, 0, 220))
        self.rect = self.image.get_rect()

        self.load()

    def load(self):
        self.tiles = []
        w, h = self.rect.size
        for y in range(0, h, self.tile_size):
            for x in range(0, w, self.tile_size):
                rect = pyg.Rect(x, y, self.tile_size, self.tile_size)
                surface = self.image.subsurface(rect)
                self.tiles.append(pyg.transform.scale(surface,
                                  (self.tile_size * self.scale,
                                   self.tile_size * self.scale)))