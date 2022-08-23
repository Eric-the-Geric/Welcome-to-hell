import pygame
from settings import *
from helper import *

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_group):
        super().__init__(group)
        
        #Player movement variables

        self.pos = pos
        self.direction = pygame.math.Vector2()
        self.speed = 7
        self.gravity = 0.2
        self.jump_height = -3
        self.jumps = 0
        self.max_jumps = 1
        # Player graphics

        self.sprite_sheet = import_full_sprite_sheet("Graphics/8x8 Spritesheet among us character.png")
        

        self.idle = self.sprite_sheet[0:3]
        self.walking_right = self.sprite_sheet[3:6]
        self.jumping = self.sprite_sheet[6:9]

        # self.idle = import_images("Graphics/Idle 64x32.png")
        # self.walking_right = import_images("Graphics/Walking.png")
        # self.jumping = import_images("Graphics/jumping.png")

        # Player properties (rects etc)

        self.image = self.idle[0]
        self.rect = self.image.get_rect(topleft=pos)

        # Collision group
        self.collision_group = collision_group

        # Animations

        self.frames = 0
        self.action = "idle"

    def get_input(self):

        keys = pygame.key.get_pressed()

        # Horizontal
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.action = "left"
            self.frames += 0.1
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.action = "right"
            self.frames += 0.1
        else:
            self.direction.x = 0
            self.action = "idle"

        # Jump
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.jumps < self.max_jumps:
                    self.direction.y = self.jump_height
                    self.action = "jump"
                    self.image = self.jumping[0]
                    self.jumps += 1


    def move(self):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        self.rect.center += self.direction*self.speed

    def animate(self):
        if self.direction.y > 0.5:
            
            self.image = self.jumping[2]

        elif self.action == "idle":
            self.image = self.idle[int(self.frames) % 2]
            self.frames += 0.1

        elif self.action == "right":
            self.image = self.walking_right[int(self.frames)%3]

        elif self.action == "left":
            self.image = pygame.transform.flip(self.walking_right[int(self.frames)%3], True, False)

    def apply_gravity(self):
        self.direction.y += self.gravity
    
    def horizontal_collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0 and abs(self.rect.left - sprite.rect.right) < 10:
                    self.rect.left = sprite.rect.right
                    # self.direction.y -= 0.07
                    self.max_jumps = 2

                if self.direction.x > 0 and abs(self.rect.right - sprite.rect.left) < 10:
                    self.rect.right = sprite.rect.left
                    # self.direction.y -= 0.07
                    self.max_jumps = 2

    def vertical_collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps = 0
                    self.max_jumps = 1
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def update(self):
        self.get_input()
        self.move()
        self.horizontal_collision()
        self.apply_gravity()
        self.vertical_collision()
        self.animate()
        
class PlayerAmongUs(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_group):
        super().__init__(group)
        
        #Player movement variables

        self.pos = pos
        self.direction = pygame.math.Vector2()
        self.speed = 7
        self.gravity = 0.2
        self.jump_height = -3
        self.jumps = 0
        self.max_jumps = 1
        # Player graphics

        self.idle = import_complicated_full_sprite_sheet("Graphics2/idle.png", 36, 48, scaling_factor, (255,127,39))
        self.walking_right = import_complicated_full_sprite_sheet("Graphics2/walking.png", 36, 48, scaling_factor, (255,127,39))
        self.jumping = import_complicated_full_sprite_sheet("Graphics2/jumping.png", 36, 48, scaling_factor, (255,127,39))

        # Player properties (rects etc)

        self.image = self.idle[0]
        self.rect = self.image.get_rect(topleft=pos)

        # Collision group
        self.collision_group = collision_group

        # Animations

        self.frames = 0
        self.action = "idle"

    def get_input(self):

        keys = pygame.key.get_pressed()

        # Horizontal
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.action = "left"
            self.frames += 0.1
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.action = "right"
            self.frames += 0.1
        else:
            self.direction.x = 0
            self.action = "idle"

        # Jump
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.jumps < self.max_jumps:
                    self.direction.y = self.jump_height
                    self.action = "jump"
                    self.image = self.jumping[0]
                    self.jumps += 1


    def move(self):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        self.rect.center += self.direction*self.speed

    def animate(self):
        if self.direction.y > 0.5:
            self.image = self.jumping[2]

        elif self.action == "idle":
            self.image = self.idle[int(self.frames) % 2]
            self.frames += 0.1

        elif self.action == "right":
            self.image = self.walking_right[int(self.frames)%3]

        elif self.action == "left":
            self.image = pygame.transform.flip(self.walking_right[int(self.frames)%3], True, False)

    def apply_gravity(self):
        self.direction.y += self.gravity
    
    def horizontal_collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0 and abs(self.rect.left - sprite.rect.right) < 10:
                    self.rect.left = sprite.rect.right
                    # self.direction.y -= 0.07
                    self.max_jumps = 2

                if self.direction.x > 0 and abs(self.rect.right - sprite.rect.left) < 10:
                    self.rect.right = sprite.rect.left
                    # self.direction.y -= 0.07
                    self.max_jumps = 2

    def vertical_collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps = 0
                    self.max_jumps = 1
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def update(self):
        self.get_input()
        self.move()
        self.horizontal_collision()
        self.apply_gravity()
        self.vertical_collision()
        self.animate()
        