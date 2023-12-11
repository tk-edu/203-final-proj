# https://pygame.readthedocs.io/en/latest/tiles/tiles.html
import os

import pygame as pyg

from tileset import *
from common import *

class Tilemap:
    def __init__(self, file: str, tileset: Tileset, size: Vec2, rect: pyg.Rect|None = None):
        self.tileset = tileset
        self.size = Vec2(int(size.x), int(size.y))
        w, h = self.size

        # The resolution of the image matches the actual
        # rendered resolution of the final display
        self.image = pyg.Surface((self.size.x * self.tileset.scale * self.tileset.tile_size,
                                  self.size.y * self.tileset.scale * self.tileset.tile_size))
        self.file = os.path.join(os.path.dirname(__file__), 'assets', file)
        with open(self.file, 'r') as map_file:
            self.map = [line.strip() for line in map_file.readlines()]

        if rect:
            self.rect = pyg.Rect(rect)
        else:
            self.rect = self.image.get_rect()
        
    # Lol, hard-coded offests into the tileset...
    def map_to_index(self, character: str) -> int|None:
        match character:
            case '-':
                return 10
            case '_':
                return 11
            case '~':
                return 13
            case '#':
                return 12
            case 'c':
                return 14
            case 'd':
                return 15
        return None
    
    def get_spawn(self) -> Vec2(int, int):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == 'S':
                    return Vec2(x, y)