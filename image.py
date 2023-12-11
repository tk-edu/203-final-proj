import os

import pygame as pyg

MAIN_DIR = os.path.dirname(__file__)

SENTIENT_SIZE = (10, 16)
ITEM_SIZE = (10, 12)

# Spritesheet images
# self.spritesheet = pygame.image.load('person.png').convert()
# self.spritesheet.set_colorkey(self.spritesheet.get_at((0, 0)))
# self.sprites = []
# self.rects = []
# # Slicing spritesheet with subsurface and rects
# for y in range(4):
#     for x in range(4):
#         rect = pygame.Rect(x * 32, y * 32, 32, 32)
#         self.sprites.append(self.spritesheet.subsurface(rect))
#         self.rects.append(rect)

class Image:
    def __init__(self, size, tile_size, scale, file):
        self.size = size
        self.file = os.path.join(MAIN_DIR, 'assets', file)
        self.tiles = []
        # match size:
        #     case Vec2(1, 1):
        #         self.rect = pyg.Rect(tile_size * scale, tile_size * scale, tile_size * scale, tile_size * scale)
        #     case Vec2(1, 2):
        #         self.rect = pyg.Rect(tile_size * scale, (tile_size * 2) * scale, tile_size * scale, tile_size * 2 * scale)
        #     case Vec2(64, 48):
        #         self.rect = pyg.Rect(tile_size * scale, (tile_size * 2) * scale, tile_size * scale, tile_size * 2 * scale)
            # case 'character_sprite':
            #     self.file = os.path.join(MAIN_DIR, 'assets', self.file)
            # case 'background_tile':
            #     self.file = os.path.join(MAIN_DIR, 'assets', self.file)
        self.surface = pyg.image.load(self.file).convert()
        # Rows
        for y in range(self.size[1]):
            # Columns
            for x in range(self.size[0]):
                rect = pyg.Rect(x, y, tile_size, tile_size)
                self.tiles.append(self.surface.subsurface(rect))