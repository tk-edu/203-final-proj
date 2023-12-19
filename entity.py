from enum import Enum

import pygame as pyg

from animation import Animation
from tilemap import *

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Entity:
    def __init__(self, id: int, speed: float, tiles: list[list[pyg.Surface]], rect: pyg.Rect, rendered_tile_size: int, animations: list[Animation] = None):
        self.id = id
        self.rect = rect
        self.prev_rect = rect
        self.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display = pyg.Surface((self.rect.width, self.rect.height))
        self.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display.set_colorkey((0, 0, 0))

        self.animations = animations

        self.tiles = tiles
        self.directions = {Direction.RIGHT}
        self.speed = speed
        self.reverse_speed = speed * 0.5 # Yes!

        self.render(rendered_tile_size)

    def render(self, rendered_tile_size: int):
        for j in range(int(self.rect.height / rendered_tile_size)):
            for i in range(int(self.rect.width / rendered_tile_size)):
                self.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display.blit(self.tiles[j][i], (i * rendered_tile_size, j * rendered_tile_size))

    def set_pos(self, x: int, y: int):
        self.prev_rect = self.rect.copy()
        self.rect.left = x
        self.rect.top = y

    def add_direction(self, direction: Direction):
        self.directions.add(direction)

    def remove_direction(self, direction: Direction):
        # Ultra inefficient
        if direction in self.directions:
            self.directions.remove(direction)
    
    def set_direction(self, direction: Direction):
        self.directions.clear()
        self.add_direction(direction)

    def is_on_ground(self, map_rects: list[pyg.Rect]):
        for map_rect in map_rects:
            for ray_len in range(1 + 1): # ? idk
                # March a ray down into the tile below the entity (`map_rect`),
                # and if it collides with the rect, we win.
                # print(f'Map rect: {map_rect=}\nTesting point: {(map_rect.centerx, self.rect.bottom + ray_len)}')
                if map_rect.collidepoint(self.rect.centerx, self.rect.bottom + ray_len):
                    return True
        return False