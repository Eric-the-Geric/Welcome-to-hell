import pygame
from settings import *
from helper import *
import random
from camera import*
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
    def __init__(self, group, pos, image, target):
        super().__init__(group)
        self.target = target
        self.group = group
        self.image_list = image
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.frames = random.randint(0,3)
        self.modded = len(self.image_list)
        self.animation_speed = (random.randint(0,10))/100
        self.particles = []
        self.max_particles = 1


    def get_distance(self):
        return pygame.math.Vector2.distance_to(pygame.math.Vector2(self.rect.center), pygame.math.Vector2(self.target.rect.center))

    def destroy_particle(self):
        if len(self.particles) > 0:

            for particle in self.particles:
                if  pygame.math.Vector2.distance_to(pygame.math.Vector2(self.rect.center), pygame.math.Vector2(particle.rect.center)) > 200:
                    self.particles.remove(particle)
                    particle.kill()
                if particle.direction.magnitude() < 1:
                    self.particles.remove(particle)
                    particle.kill()
    def animate(self):
        self.image = self.image_list[(int(self.frames) + self.modded) % self.modded]
        self.frames += self.animation_speed
    
    def create_particles(self):
        distance = self.get_distance()
        if  distance < 200 and len(self.particles) < self.max_particles:
            self.particles.append(Particle(self.rect.center, self.group, "Graphics2/lava particle.png"))
            self.group[2].remove(self.particles[-1])
    
    def update(self):
        self.animate()
        self.create_particles()
        self.destroy_particle()

        

class Meteor(AnimatedTile):
    def __init__(self, group, pos, image, collision_group, target):
        super().__init__(group, pos, image, target)
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
                # self.rect.centery = 4000
                self.kill()

    def update(self):
        self.collision()
        self.animate()
        self.gravity()
        self.move()
        if self.rect.centery > 2700:
            self.kill()

class WireEnemy(AnimatedTile):
    def __init__(self, group, pos, image, target, camera_group, harmful_group):
        super().__init__(group, pos, image, target)
        self.camera_group = camera_group
        self.harmful_group = harmful_group
        self.target = target
        self.zonex = self.image.get_width()*15
        self.zoney = self.image.get_height()*15
        self.zonerect = pygame.Rect(self.rect.centerx-(self.zonex//2), self.rect.centery-(self.zoney//2), self.zonex, self.zoney)
        self.surface = pygame.display.get_surface()
        self.pos = pygame.math.Vector2(pos)
        
        self.animation_speed = 0.12
        self.direction = pygame.math.Vector2()
        self.max_bullets = 1
        self.bullets = []


    def found_player(self, target_pos):
        if pygame.Rect.colliderect(self.target.rect, self.zonerect):
            if len(self.bullets) < self.max_bullets:
                #Gets the direction on the player
                target_vector = pygame.math.Vector2(target_pos)
                self.direction =  target_vector - self.pos
                self.direction = self.direction.normalize()
                self.bullets.append(Bullet(self.pos, [self.camera_group, self.harmful_group], "Graphics2/lighting_particle.png"))
            
            
    def shoot(self):
        for bullet in self.bullets:
            bullet.update(self.direction)
            if pygame.math.Vector2.distance_to(pygame.math.Vector2(self.rect.center), pygame.math.Vector2(bullet.rect.center)) > 1000:
                self.bullets.remove(bullet)
                bullet.kill()
                
                
            
    def update(self, target_pos):
        self.animate()
        self.found_player(target_pos)
        self.shoot()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, group, path):
        super().__init__(group)
        self.pos = pos
        self.image = import_complicated_full_sprite_sheet(path, 9, 14, (255,127,39))[0]
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(topleft = (pos))
        self.speed = 10

    def shoot(self, direction):
        self.rect.center += direction*self.speed

    def update(self, direction):
        self.shoot(direction)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, group, path):
        super().__init__(group)
        self.speed = random.randint(1,4)
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.image = import_complicated_full_sprite_sheet(path, 12, 12, (255,127,39))[0]
        # self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(topleft = (pos))
    
    
    def shoot(self):
        self.rect.center += self.direction*self.speed
    
    def update(self):
        
        self.shoot()