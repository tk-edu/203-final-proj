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
"""The size in pixels of each tile"""
SCALE     =    4
REN_TILE_SIZE = TILE_SIZE * SCALE
"""The size in pixels of each tile after scaling"""

FPS       = 60

PIXEL     = 1

FONT      = 'CozetteVector'
FONT_SIZE = 30
# 16 x 12 tiles
TILES_W   = int(WIDTH  / TILE_SIZE) / SCALE
TILES_H   = int(HEIGHT / TILE_SIZE) / SCALE

X_VELOCITY = 1
Y_VELOCITY = 20
JUMP = False

FRAME_ADVANCE = False

BASE_ACCEL = 1

RUN = 1.5

class Game:
    def __init__(self, title, width = WIDTH, height = HEIGHT):
        pyg.init()
        font = pyg.font.SysFont(FONT, FONT_SIZE)

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
        self.debug_surface = pyg.Surface((0, 0))
        self.intersection_rect = pyg.Rect(0, 0, 0, 0)
        # The TILES index!!! (yes i agree) is very much so indeed
        # based on the OFFSET INTO THE tileset.png file in which
        # our tile asSets are Being stored! so Don't Ask me where
        # thesE numb eres came from.!
        spawn_position = self.tilemap.get_spawn()
        self.player = Entity(0, 5, [[self.tileset.tiles[5]], [self.tileset.tiles[6]]],
                             pyg.Rect((spawn_position.x * REN_TILE_SIZE, spawn_position.y * REN_TILE_SIZE),
                                      (REN_TILE_SIZE, REN_TILE_SIZE * 2)), REN_TILE_SIZE)
        self.entities.append(self.player)

        #hopefully make an enemy
        elf_spawn_position = self.tilemap.get_elf_spawn()
        self.elf = Entity(1, 4, [[self.tileset.tiles[0]], [self.tileset.tiles[2]]],
                          pyg.Rect((elf_spawn_position.x * REN_TILE_SIZE, elf_spawn_position.y * REN_TILE_SIZE),
                                   (REN_TILE_SIZE, REN_TILE_SIZE * 2)), REN_TILE_SIZE)
        self.entities.append(self.elf)

        self.background = pyg.image.load('assets/sky_2.png').convert()
        # self.background.set_colorkey((254, 245, 238))
        self.background_rect = self.background.get_rect()
        # pyg.display.set_mode(self.background_rect.size)

        self.offset = Vec2(0, 0)

    def draw_tiles(self):
        map_rects = []
        for j in range(self.tilemap.size.y):
            for i in range(self.tilemap.size.x):
                index = self.tilemap.map_to_index(self.tilemap.map[j][i])
                # If there's an index without a tile (according
                # to the hard-coded `map_to_index` function), then
                # it'll be "transparent" because we're not going to blit it
                if index != None:
                    tile = self.tileset.tiles[index]
                    rect = pyg.Rect(i * REN_TILE_SIZE + self.offset.x,
                                    j * REN_TILE_SIZE + self.offset.y,
                                    REN_TILE_SIZE, REN_TILE_SIZE)
                    self.screen.blit(tile, rect)
                    # Don't give clouds collision (DGCC)
                    if index != 14 and index != 15:
                        map_rects.append(rect)
        self.map_rects = map_rects

    def draw_title_text(self):
        self.title_text.flash_colors(color.RED, color.GREEN, 100)
        self.screen.blit(self.title_text.surface, (WIDTH / 2 - self.title_text.surface.get_rect().centerx,
                                                   HEIGHT / 2 - self.title_text.surface.get_rect().centery))

    def __draw_fps(self):
        self.__fps_text.update(str(int(self.clock.get_fps())))
        self.screen.blit(self.__fps_text.surface, (0, 0))
    
    def draw_entities(self):
        for entity in self.entities:
            render_surface = entity.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display
            if Direction.LEFT in entity.directions:
                render_surface = pyg.transform.flip(entity.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display, True, False)
            self.screen.blit(render_surface, pyg.Rect(entity.rect.left, entity.rect.top, entity.rect.width, entity.rect.height))

    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        self.draw_tiles()
        self.draw_entities()
        # self.draw_title_text()
        self.screen.fill((255, 0, 0), self.intersection_rect)
        self.__draw_fps()

        pyg.display.flip()

    def move_player(self, speed: float, x_offset: int = 0, y_offset: int = 0, change_direction: bool = True):
        self.player.set_pos(self.player.rect.x + x_offset * speed, self.player.rect.y + y_offset)
        if change_direction:
            if x_offset < 0:
                self.player.set_direction(Direction.LEFT)
            elif x_offset >= 1:
                self.player.set_direction(Direction.RIGHT)

    def move_enemies(self, speed: float, x_offset: int = 1, y_offset: int = 0):
        distance_x = self.player.rect.x - self.elf.rect.x
        distance_y = self.player.rect.y - self.elf.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** .5
        if self.elf.is_on_ground(self.map_rects):
            ...
        elif not self.elf.is_on_ground(self.map_rects):
            ...
        if distance_x < 0:
            self.elf.set_direction(Direction.RIGHT)
        elif distance_x >= 1:
            self.elf.set_direction(Direction.LEFT)
        #TODO for some reason it doesn't work when player 
        #distance is specified don't ask me why, I literally 
        #have no idea. Anyway fix that and also add gravity.
        #if distance < 200:
        if distance != 0:
                #self.elf.set_pos(self.elf.rect.x + speed * distance_x / distance, self.elf.rect.y + y_offset)
            self.elf.rect.x += speed * distance_x / distance
                #self.elf.rect.y += speed * distance_y / distance
            

    # TODO: use pyg.Sprite
    def resolve_player_collision(self):
        for tile_rect in self.map_rects:
            intersection = tile_rect.clip(self.player.rect)
            if intersection.width:
                self.intersection_rect = intersection
                print(f'[\t{intersection.left=}, {self.player.rect.right=}\n\t{intersection.right=}, {self.player.rect.left=}\n]')
            if intersection.left   <   self.player.rect.left:   self.move_player(self.player.speed, x_offset=-intersection.width, change_direction=False); #self.intersection_rect = intersection
            if intersection.right  >   self.player.rect.right:  self.move_player(self.player.speed, x_offset=intersection.width, change_direction=False); #self.intersection_rect = intersection
            if intersection.top    <=  self.player.rect.top:    self.move_player(self.player.speed, y_offset=intersection.height, change_direction=False)
            if intersection.bottom >=  self.player.rect.bottom: self.move_player(self.player.speed, y_offset=-intersection.height, change_direction=False)

    def resolve_enemy_collsions(self):
        ...

    def resolve_object_collisions(self, x_position, y_position):
        ...

    def resolve_collisions(self):
        self.resolve_player_collision()
        # self.resolve_enemy_collsions()
        # self.resolve_object_collisions()

    # https://stackoverflow.com/a/55321731
    def scrollX(self, screenSurf, offsetX):
        width, height = screenSurf.get_size()
        copySurf = screenSurf.copy()
        screenSurf.blit(copySurf, (offsetX, 0))
        if offsetX < 0:
            screenSurf.blit(copySurf, (width + offsetX, 0), (0, 0, -offsetX, height))
        else:
            screenSurf.blit(copySurf, (0, 0), (width - offsetX, 0, offsetX, height))

    def scroll_screen(self, direction: Direction):
        if self.player.rect.centerx >= WIDTH / 2:
            if direction == Direction.LEFT:
                self.scrollX(self.background, 10)
                # self.background.scroll(10, 0)
            elif direction == Direction.RIGHT:
                self.scrollX(self.background, -10)
                # self.background.scroll(-10, 0)

    def run(self):
        global JUMP, Y_VELOCITY
        keys = pyg.key.get_pressed()

        player_speed = self.player.speed
        elf_speed  = self.elf.speed

        if keys[pyg.K_LSHIFT]:
            player_speed *= RUN

        # We're doing great!
        if JUMP is False and keys[pyg.K_SPACE]:
            JUMP = True
        if JUMP is True:
            Y_VELOCITY -= 1
            self.move_player(player_speed, y_offset=-Y_VELOCITY)
            if self.player.is_on_ground(self.map_rects):
                JUMP = False
                Y_VELOCITY = 20

        if not JUMP and not self.player.is_on_ground(self.map_rects):
            self.move_player(player_speed, y_offset=Y_VELOCITY)

        if keys[pyg.K_a]:
            # self.scroll_screen(Direction.LEFT)
            # Start scrolling back once we're 6 tiles from the left, but
            # stop if we get too close to the left edge of the screen
            if self.player.rect.centerx <= REN_TILE_SIZE * 6:
                speed_modifier = 1
                if player_speed == self.player.speed * RUN:
                    speed_modifier = RUN
                elif player_speed == self.player.reverse_speed:
                    speed_modifier = 0.5
                self.offset.x += player_speed
            else:
                if Direction.RIGHT in self.player.directions:
                    player_speed = self.player.reverse_speed
                if self.player.is_on_ground(self.map_rects):
                    self.move_player(player_speed, x_offset=-1)
                else:
                    self.move_player(player_speed, x_offset=-1, change_direction=False)

        elif keys[pyg.K_d]:
            # self.scroll_screen(Direction.RIGHT)
            # Start scrolling forward once we're at the center of the screen
            if self.player.rect.centerx >= WIDTH / 2:
                speed_modifier = 1
                if player_speed == self.player.speed * RUN:
                    speed_modifier = RUN
                elif player_speed == self.player.reverse_speed:
                    speed_modifier = 0.5
                self.offset.x -= player_speed
            else:
                if Direction.LEFT in self.player.directions:
                    player_speed = self.player.reverse_speed
                if self.player.is_on_ground(self.map_rects):
                    self.move_player(player_speed, x_offset=1)
                else:
                    self.move_player(player_speed, x_offset=1, change_direction=False)

        # if keys[pyg.K_s]:
        #     self.player.tiles = [[self.tileset.tiles[8]]]
        #     self.player.rect = pyg.Rect(self.player.rect.left, self.player.rect.top + REN_TILE_SIZE, REN_TILE_SIZE, REN_TILE_SIZE)
        #     self.player.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display.fill((0, 0, 0))
        #     self.player.render(REN_TILE_SIZE)
        # else:
        #     self.player.tiles = [[self.tileset.tiles[5]], [self.tileset.tiles[6]]]
        #     self.player.rect = pyg.Rect(self.player.rect.left, self.player.rect.top, REN_TILE_SIZE, REN_TILE_SIZE * 2)
        #     self.player.surface_that_we_will_render_the_tiles_onto_such_that_they_will_be_properly_placed_onto_the_final_display.fill((0, 0, 0))
        #     self.player.render(REN_TILE_SIZE)
        self.move_enemies(2)
        self.resolve_collisions()
        #self.move_enemies(elf_speed)
        self.draw()
        self.screen.blit(self.debug_surface, (WIDTH - self.intersection_rect.width, self.intersection_rect.height))
        self.clock.tick(self.fps)
    
if __name__ == '__main__':
    game = Game("Holiday Adventure 1: Santa's Last Wish - Starring Kandy Kayne")
    frame_advance_count = 0
    exit = False
    while not exit:
        for event in pyg.event.get():
            match event.type:
                case pyg.KEYDOWN:
                    if event.key == pyg.K_f:
                        pyg.key.set_repeat(125)
                        if not FRAME_ADVANCE:
                            FRAME_ADVANCE = True
                            print('frame advance on ', end='\r')
                        else:
                            frame_advance_count += 1
                            print(f'frame advance on ({frame_advance_count})', end='\r')
                            game.run()
                    elif FRAME_ADVANCE and event.key == pyg.K_p:
                        pyg.key.set_repeat(0)
                        frame_advance_count = 0
                        print('\nframe advance off')
                        FRAME_ADVANCE = False
                case pyg.QUIT:
                    exit = True
        if not FRAME_ADVANCE:
            game.run()
    pyg.quit()
# https://github.com/kidscancode/pyg_tutorials/blob/master/tilemap/part%2001/main.py