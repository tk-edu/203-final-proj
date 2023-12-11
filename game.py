import threading
import os

import pygame as pyg

import color
from text import Text
from tileset import *
from tilemap import *
from entity import *
from common import *
from image import *

WIDTH     = 1024
HEIGHT    =  768
TILE_SIZE =   16
SCALE     =    4
REN_TILE_SIZE = TILE_SIZE * SCALE

FPS       = 60

PIXEL     = 1

FONT      = 'CozetteVector'
FONT_SIZE = 30
# 16 x 12 tiles
TILES_W   = int(WIDTH  / TILE_SIZE) / SCALE
TILES_H   = int(HEIGHT / TILE_SIZE) / SCALE

X_VELOCITY = 1
Y_VELOCITY = 10
JUMP = False

class Game:
    def __init__(self, title, width = WIDTH, height = HEIGHT):
        pyg.init()
        font = pyg.font.SysFont('CozetteVector', FONT_SIZE)

        self.screen = pyg.display.set_mode((width, height))
        pyg.display.set_caption(title)

        self.clock = pyg.time.Clock()
        self.fps = FPS

        self.tileset = Tileset('tileset.png', TILE_SIZE, SCALE)
        self.tilemap = Tilemap('level_1.map', self.tileset, Vec2(TILES_W, TILES_H))

        self.title_text = Text("Holiday Adventure 1: Santa's Last Wish - Starring Kandy Kayne", FONT, FONT_SIZE, color.WHITE, False)
        self.__fps_text = Text(str(int(self.clock.get_fps())), FONT, FONT_SIZE, color.YELLOW, False)

        # Rects to be used for collision detection
        self.map_rects = []
        self.entities = []
        # The TILES index!!! (yes i agree) is very much so indeed
        # based on the OFFSET INTO THE tileset.png file in which
        # our tile asSets are Being stored! so Don't Ask me where
        # thesE numb eres came from.!
        spawn_position = self.tilemap.get_spawn()
        self.player = Entity(0, 7, [[self.tileset.tiles[5]], [self.tileset.tiles[6]]], pyg.Rect((spawn_position.x * REN_TILE_SIZE, spawn_position.y * REN_TILE_SIZE), (REN_TILE_SIZE, REN_TILE_SIZE * 2)), REN_TILE_SIZE)
        self.entities.append(self.player)

        self.background = pyg.image.load('assets/sky_2.png').convert()
        self.background_rect = self.background.get_rect()
        # pyg.display.set_mode(self.background_rect.size)

    def draw_tiles(self):
        for j in range(self.tilemap.size.y):
            for i in range(self.tilemap.size.x):
                index = self.tilemap.map_to_index(self.tilemap.map[j][i])
                # If there's an index without a tile (according
                # to the hard-coded `map_to_index` function), then
                # it'll be "transparent" because we're not going to blit it
                if index != None:
                    tile = self.tileset.tiles[index]
                    rect = pyg.Rect(i * REN_TILE_SIZE, j * REN_TILE_SIZE,
                                    REN_TILE_SIZE, REN_TILE_SIZE)
                    self.screen.blit(tile, rect)
                    self.map_rects.append(rect)

    def draw_title_text(self):
        self.title_text.flash_colors(color.RED, color.GREEN, 100)
        self.screen.blit(self.title_text.surface, (WIDTH / 2 - self.title_text.surface.get_rect().centerx,
                                                   HEIGHT / 2 - self.title_text.surface.get_rect().centery))

    def __draw_fps(self):
        self.__fps_text.update(str(int(self.clock.get_fps())))
        self.screen.blit(self.__fps_text.surface, (0, 0))
    
    # # https://stackoverflow.com/a/4935466
    # def range_with_float_step(self, start, stop, step):
    #     num_elements = int((stop - start) / float(step))
    #     for i in range(num_elements + 1):
    #         yield start + i * step

    def draw_entities(self):
        for entity in self.entities:
            self.screen.blit(entity.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display, pyg.Rect(entity.rect.left, entity.rect.top, entity.rect.width, entity.rect.height))

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.draw_tiles()
        self.draw_entities()
        self.draw_title_text()
        self.__draw_fps()
        pyg.display.flip()

    def move_player(self, x_offset = 0, y_offset = 0):
        new_rect = pyg.Rect(self.player.rect.x + x_offset * self.player.speed, self.player.rect.y + y_offset * self.player.speed, self.player.rect.width, self.player.rect.height)
        self.player.rect = new_rect
        print(new_rect)

    def move_enemies(self):
        ...

    def has_intersection(self, pos_1, pos_2):
        intersection = (None, None)
        if pos_1[0] == pos_2[0]:
            intersection.x = pos_1[0]
        if pos_1[1] == pos_2[1]:
            intersection.y = pos_1[1]
        return intersection

    def resolve_player_collision(self):
        for row in self.curr_level.map:
            for column in row:
                if column == '#' or column == '-':
                    # Push the player out of places they shouldn't be!
                    intersection = self.has_intersection(self.player.pos, (row, column))
                    x_offset = 0
                    y_offset = 0
                    for direction in self.player.directions:
                        match direction:
                            case direction.UP:
                                y_offset -= 1
                            case direction.DOWN:
                                y_offset += 1
                            case direction.LEFT:
                                x_offset -= 1
                            case direction.RIGHT:
                                x_offset += 1
                    if intersection.x:
                        self.move_player(x_offset=x_offset)
                    if intersection.y:
                        self.move_player(y_offset=-y_offset)

    def resolve_enemy_collsions(self):
        ...

    def resolve_object_collisions(self, x_position, y_position):
        #prevents character from going past right wall
        if x_position >= (WIDTH - PIXEL):
            x_position = (WIDTH - PIXEL)
        #prevents characetr from going past left wall
        if x_position >= 0:
            x_positon = 0
        #prevents character from going past bottom
        if y_position >= (HEIGHT - PIXEL):
            y_positon = (HEIGHT - PIXEL)
        #prevents chsrscter from going past top
        if y_positon >= 0:
            y_positon = 0

    def resolve_collisions(self):
        self.resolve_player_collision()
        self.resolve_enemy_collsions()
        self.resolve_object_collisions()

    def run(self):
        global JUMP, Y_VELOCITY
        keys = pyg.key.get_pressed()

        if keys[pyg.K_a]:
            self.move_player(x_offset=-1)
        elif keys[pyg.K_d]:
            self.move_player(x_offset=1)

        # TODO: yeah, jumping is broke af
        if JUMP is False and keys[pyg.K_SPACE]:
            JUMP = True
        if JUMP is True:
            Y_VELOCITY -= 1
            self.move_player(y_offset=-Y_VELOCITY)
            if Y_VELOCITY <= -9:
                JUMP = False
                Y_VELOCITY = 10

        # TODO: make crouch sprite
        if keys[pyg.K_s]:
            self.move_player(y_offset=1)

        # self.resolve_collisions()
        self.draw()
        self.clock.tick(self.fps)
    
if __name__ == '__main__':
    game = Game("Holiday Adventure 1: Santa's Last Wish - Starring Kandy Kayne")
    exit = False
    while not exit:
        for event in pyg.event.get():
            match event.type:
                case pyg.QUIT:
                    exit = True
        game.run()
    pyg.quit()
# https://github.com/kidscancode/pyg_tutorials/blob/master/tilemap/part%2001/main.py