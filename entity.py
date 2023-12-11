from enum import Enum

import pygame as pyg

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Entity:
    def __init__(self, id: int, speed: float, tiles: list[list[pyg.Surface]], rect: pyg.Rect, rendered_tile_size: int):
        self.id = id
        self.rect = rect
        self.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display = pyg.Surface((self.rect.width, self.rect.height))
        self.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display.set_colorkey((0, 0, 0))

        self.tiles = tiles
        self.directions = {Direction.LEFT}
        self.speed = speed

        self.render(rendered_tile_size)

    def render(self, rendered_tile_size: int):
        for j in range(int(self.rect.height / rendered_tile_size)):
            for i in range(int(self.rect.width / rendered_tile_size)):
                self.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display.blit(self.tiles[j][i], (i * rendered_tile_size, j * rendered_tile_size))

    def set_pos(self, x, y):
        self.rect.left = x
        self.rect.top = y

    def add_direction(self, direction):
        self.directions.add(direction)

    def remove_direction(self, direction):
        self.directions.remove(direction)