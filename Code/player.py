import pygame
from settings import *
from helper import *
from tile import *
from sound_effects import SoundEffects
class PlayerAmongUs(pygame.sprite.Sprite):
    def __init__(self, group, pos, collision_group, harmful_group, ship_group, music_box):
        super().__init__(group)
        self.group = group
        self.surface = pygame.display.get_surface()
        self.music_effects = SoundEffects()
        self.music_box = music_box
        self.ending_song = True
        
        #death counter
        self.offset = pygame.math.Vector2()

        #FPS counter
        self.offset2 = pygame.math.Vector2()
        #Player movement variables

        self.pos = pos
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.gravity = 0.15
        self.jump_height = -3
        self.jumps = 0
        self.max_jumps = 2
        self.death_counter = -1
        self.ending = False
        # Player graphics

        self.idle = import_complicated_full_sprite_sheet("Graphics2/idle.png", 36, 48, (255,127,39))
        self.walking_right = import_complicated_full_sprite_sheet("Graphics2/walking.png", 36, 48, (255,127,39))
        self.jumping = import_complicated_full_sprite_sheet("Graphics2/jumping.png", 36, 48, (255,127,39))

        # Player properties (rects etc)

        self.image = self.idle[0]
        self.rect = self.image.get_rect(topleft=pos)

        # Collision group & harmful_group
        self.collision_group = collision_group
        self.harmful_group = harmful_group
        self.ship_group = ship_group
        # Animations

        self.frames = 0
        self.action = "right"
        self.frame_speed = 0.1
        
        # finalle explosion
        self.particle_images= break_the_image(self.image, 5, 5)
        self.particles = []

    def create_particles(self):
        self.group[1].remove(self)
        self.speed = 0
        for i in range(len(self.particle_images)):
            self.particles.append(((MeteorParticle((self.rect.center), self.group[1], self.particle_images, i))))

    def get_input(self, events, can_move):
        if can_move:
            if not self.ending:
                keys = pygame.key.get_pressed()
                self.frames += self.frame_speed
                if keys[pygame.K_ESCAPE]:
                    self.pause = True
                # Horizontal

                if keys[pygame.K_a]:
                    self.direction.x = -1
                    self.action = "left"
                    
                elif keys[pygame.K_d]:
                    self.direction.x = 1
                    self.action = "right"
                else:
                    self.direction.x = 0
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w and self.jumps < self.max_jumps:
                            self.direction.y = self.jump_height
                            self.image = self.jumping[0]
                            self.jumps += 1


    def move(self):
        if self.direction.magnitude() != 0:
            self.direction.normalize()
        self.rect.center += self.direction*self.speed

    def animate(self):
        if self.direction.y > 0.5 and self.action == "right":
            self.image = self.jumping[2]

        elif self.direction.y > 0.5 and self.action == "left":
            self.image = pygame.transform.flip(self.jumping[2], True, False)

        elif self.direction.x == 0 and self.action == "right":
            self.image = self.idle[int(self.frames) % 2]
        
        elif self.direction.x == 0 and self.action == "left":
            self.image = pygame.transform.flip(self.idle[int(self.frames) % 2], True, False)
            
        elif self.direction.x > 0 and self.action == "right":
            self.image = self.walking_right[int(self.frames)%3]

        elif self.direction.x < 0 and self.action == "left":
            self.image = pygame.transform.flip(self.walking_right[int(self.frames)%3], True, False)

    def apply_gravity(self):
        self.direction.y += self.gravity
    
    def horizontal_collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0 and abs(self.rect.left - sprite.rect.right) < 10:
                    self.rect.left = sprite.rect.right
                    self.max_jumps = 2


                if self.direction.x > 0 and abs(self.rect.right - sprite.rect.left) < 10:
                    self.rect.right = sprite.rect.left
                    self.max_jumps = 2

    def vertical_collision(self):
        for sprite in self.collision_group.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps = 0
                    self.max_jumps = 2
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
                    
    def kill_player(self):
        if self.rect.y > 10000:
            self.rect.topleft = (12*32, 1300)
            self.death_counter += 1
            self.music_effects.play_song("death")
        for sprite in self.harmful_group.sprites():
            if sprite.rect.colliderect(self.rect):
                self.rect.topleft = (12*32, 1300)
                self.death_counter += 1
                self.music_effects.play_song("death")
    def win_level(self):
        for sprite in self.ship_group:
            if sprite.rect.colliderect(self.rect):
                self.create_particles()
                self.ending = True
                self.you_won()
                
    def you_won(self):
        if self.ending and self.ending_song:
            self.music_box.stop_song
            self.music_box.play_song("end", 0.5)
            self.ending_song = False
        font = pygame.font.Font(None, 45)
        text = font.render("Congrats you finally won the game! I hope you enjoyed!!!", True, ('white'))
        textRect = text.get_rect()
        self.offset.x += (self.rect.centerx - self.offset.x - (screen_width//2))
        self.offset.y += (self.rect.centery+300 - self.offset.y - (screen_height//2))
        textRect.center = (self.rect.topleft - self.offset)
        self.surface.blit(text, textRect)
        
        for sprite in self.particles:
            sprite.update()
    def death_score(self):
        font = pygame.font.Font(None, 45)
        text = font.render("DEATHS: " + str(self.death_counter), True, ('white'))
        textRect = text.get_rect()
        self.offset.x += (self.rect.centerx+540 - self.offset.x - (screen_width//2))
        self.offset.y += (self.rect.centery+300 - self.offset.y - (screen_height//2))
        textRect.center = (self.rect.topleft - self.offset)
        self.surface.blit(text, textRect)

    def update(self, event_list, can_move):
        self.win_level()
        self.death_score()
        self.get_input(event_list, can_move)
        self.move()
        self.horizontal_collision()
        self.apply_gravity()
        self.vertical_collision()
        self.animate()
        self.kill_player()
        
