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

class Meteor(AnimatedTile):
    def __init__(self, group, pos, image, collision_group):
        super().__init__(group, pos, image)
        self.falling_speed = random.randint(4,6)
        self.pos = pos
        self.direction = pygame.math.Vector2()
        self.collision_group = collision_group
        self.animation_speed = 0.1
    
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        self.rect.center += self.direction


    def gravity(self):
        self.direction.y = self.falling_speed

    def collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                self.rect.centery = 4000
    def update(self):
        self.collision()
        self.animate()
        self.gravity()
        self.move()

class WireEnemy(AnimatedTile):
    def __init__(self, group, pos, image, target):
        super().__init__(group, pos, image)
        self.target = target
        self.zonex = self.image.get_width()*10
        self.zoney = self.image.get_height()*10
        self.zonerect = pygame.Rect(self.rect.centerx-(self.zonex//2), self.rect.centery-(self.zoney//2), self.zonex, self.zoney)
        self.surface = pygame.display.get_surface()
        self.pos = pygame.math.Vector2(pos)
        
        self.animation_speed = 0.12
        self.direction = pygame.math.Vector2()
        self.bullets = []


    def found_player(self, target_pos):
        if pygame.Rect.colliderect(self.target.rect, self.zonerect):
            # Gets the direction on the player
            target_vector = pygame.math.Vector2(target_pos)
            direction_x = self.pos.x - target_vector.x
            direction_y = self.pos.y - target_vector.y
            self.direction.update((direction_x, direction_y))
            
            self.direction = self.direction.normalize()

            
            
            
    def update(self, target_pos):
        self.animate()
        self.found_player(target_pos)
        for bullet in self.bullets:
            bullet.update()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init()
        self.pos = pos
        self.image = import_complicated_full_sprite_sheet("Graphics2/lightning_particle.png", 9, 14, (255,127,39))[0]
        self.rect = self.image.get_rect(topleft = (pos))
        self.speed = 10

    def shoot(self, direction):
        self.rect.center += direction*self.speed

    def update(self):
        self.shoot()
