import pygame
from settings import *
from helper import *
import random
class Tile(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.tiles = import_images("Graphics/background and map.png")
        
class TerrainTile1(Tile):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image= self.tiles[2]
        self.rect = self.image.get_rect(topleft = pos)

class TerrainTile2(Tile):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image= self.tiles[3]
        self.rect = self.image.get_rect(topleft = pos)

class Clouds1(Tile):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image= self.tiles[4]
        self.rect = self.image.get_rect(topleft = pos)

class Clouds2(Tile):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image= self.tiles[5]
        self.rect = self.image.get_rect(topleft = pos)

class Stars(Tile):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image= self.tiles[1]
        self.rect = self.image.get_rect(topleft = pos)

class Background(Tile):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image= self.tiles[0]
        self.rect = self.image.get_rect(topleft = pos)


class StaticTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        

class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image_list = image
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frames = random.randint(0,3)
        self.modded = len(self.image_list)
        self.animation_speed = (random.randint(0,10))/100
    def animate(self):
        self.image = self.image_list[(int(self.frames) + self.modded) % self.modded]
        self.frames += self.animation_speed
    def update(self):
        self.animate()