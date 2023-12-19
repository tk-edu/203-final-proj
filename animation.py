import pygame as pyg

class Animation:
    def __init__(self):
        ...

    def kayne_walking(self):
        #check if character is moving
        moving = False
        value = 0
        frames = [self.tilset.tiles[6], self.tileset.tiles[7]]

        if value > len(frames):
            value = 0
        
        #check if the character is moving
        keys = pyg.key.get_pressed()
        if keys[pyg.K_A] or keys[pyg.K_D]:
            moving = True
        #if moving iterate through the animation frames
        if moving:
            value += 1

        #grab current frame to blit 
        curr_image = frames[value]

    #make elf walking animation
    def elf_walking(self):
        value = 0
        frames = [self.tileset.tiles[2], self.tileset.tiles[3], self.tileset.tiles[2], self.tileset.tiles[4]]

        if value > len(frames):
            value = 0

        value += 1
        curr_image = frames[value]
    def update(self):
        ...