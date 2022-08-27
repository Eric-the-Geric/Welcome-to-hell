import pygame
from helper import *
from settings import *
from level_data import *
from tile import *
from player import PlayerAmongUs
from camera import *
from button import *
import random
from sound_effects import SoundEffects
# Finish the level
# add Enemies
# add sounds
class Level_1:

    def __init__(self, music_box):
        # Get the surface
        self.surface = pygame.display.get_surface()
        self.music_box = music_box
        self.music_effects = SoundEffects()
        
        # Setting up sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.visible_group = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        self.animated_group = pygame.sprite.Group()
        self.meteor_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.harmful_group = pygame.sprite.Group()
        self.enemy_wires_group = pygame.sprite.Group()
        self.ship_group = pygame.sprite.Group()


        # Getting the layout data
        self.player_layout = import_map_data(Level_2["Player"])
        self.lava_layout = import_map_data(Level_2["Lava"])
        self.terrain_layout = import_map_data(Level_2["Terrain"])
        self.spikes_layout = import_map_data(Level_2["Spikes"])
        self.volcano_layout = import_map_data(Level_2["Volcano"])
        self.boddies_layout = import_map_data(Level_2["Boddies"])
        self.mask_layout = import_map_data(Level_2["Masks"])
        self.enemy_wires_layout = import_map_data(Level_2["Enemy_wires"])
        self.space_ship_layout = import_map_data(Level_2["Space_ship"])


        # Setting up images   
        self.lava_image = import_complicated_full_sprite_sheet("Graphics2/lava block - Copy.png",
                                                            32, 32, (255,127,39))
        self.terrain_image = import_complicated_full_sprite_sheet("Graphics2/grass.png",
                                                            32, 32, (255,127,39))
        self.spikes_image = import_complicated_full_sprite_sheet("Graphics2/rockspikes.png",
                                                            81, 63, (255,127,39))
        self.volcano_image = import_complicated_full_sprite_sheet("Graphics2/volcano.png",
                                                            110, 52, (255,127,39))
        self.boddies_image = import_complicated_full_sprite_sheet("Graphics2/dead.png",
                                                            31, 34, (255,127,39))                                                        
        self.mask_image = import_complicated_full_sprite_sheet("Graphics2/masks.png",
                                                            51, 51, (255,127,39))                                                     
        self.meteor_image = import_complicated_full_sprite_sheet("Graphics2/Meteor.png",
                                                            134, 187, (255,127,39))
        self.enemy_wires_image = import_complicated_full_sprite_sheet("Graphics2/wires_enemy.png",
                                                            32, 32, (255,127,39))
        self.ship_image = import_complicated_full_sprite_sheet("Graphics2/space_ship.png",
                                                            221, 137, (255,127,39))
       

        # Setting up sprites
        self.space_ship = self._create_terrain(self.space_ship_layout, "ship", tile_size, tile_size, self.ship_image)
        
        self.player = self._create_player(self.player_layout, 48, 36)
        
        self.spikes =  self._create_terrain(self.spikes_layout, "spikes", tile_size, tile_size, self.spikes_image)
        
        self.volcano =  self._create_terrain(self.volcano_layout, "volcano", tile_size, tile_size, self.volcano_image)
        
        self.terrain = self._create_terrain(self.terrain_layout, "terrain", tile_size, tile_size, self.terrain_image)

        self.boddies =  self._create_terrain(self.boddies_layout, "boddies", tile_size, tile_size, self.boddies_image)
        
        self.masks =  self._create_terrain(self.mask_layout, "masks", tile_size, tile_size, self.mask_image)
        
        

        # Lava and meteor later so it renders over the player
        self.enemy_wires = self._create_terrain(self.enemy_wires_layout, "wires", tile_size, tile_size, self.enemy_wires_image)
        self.lava = self._create_terrain(self.lava_layout, "lava", tile_size, tile_size, self.lava_image)
        

        
        self.font = pygame.font.Font(None, 32)
        self.play_intro = True
        self.play_main_song_loop = True
        self.easter_egg = True
        self.ten_deaths = True
        self.intro_timer = 0
        self.can_move = False

    def run(self, event_list):
        
        if self.play_intro:
            self.music_box.stop_song()
            self.music_box.play_song("intro", volume = 0.5)
            self.play_intro = False
            self.play_main_song_loop = True
        self.intro_timer += 0.5

        if self.intro_timer > 1320 and self.play_main_song_loop:
            self.can_move = True
            self.music_box.stop_song()
            self.music_box.play_song("game",0.1, True)
            self.play_main_song_loop = False

        if self.player.rect.centerx < 3*32 and self.easter_egg:
            self.music_box.stop_song()
            self.intro_timer = 920
            self.music_box.play_song("egg")
            self.play_main_song_loop = True
            self.easter_egg = False

        if self.player.death_counter == 10 and self.ten_deaths:
            self.music_box.stop_song()
            self.intro_timer = 1070
            self.music_box.play_song("ten")
            self.play_main_song_loop = True
            self.ten_deaths = False
        
            
        
        number = 1
        pos = (0,0)
        if self.player.rect.centery < 30*tile_size:
            number = random.randint(1, 60)
            pos = (random.randint(32*tile_size, 53*tile_size), 0)
        elif self.player.rect.centery > 55*tile_size:
            number = random.randint(1, 30)
            pos = (random.randint(30*tile_size, 90*tile_size), 50*tile_size)
        
        self._create_meteor(number, pos)
        
        self.animated_group.update()
        self.meteor_group.update()
        self.camera_group.custom_draw(self.player)
        self.player_group.update(event_list, self.can_move)
        self.enemy_wires_group.update(self.player.rect.center)
        
        
    def _create_meteor(self, number, pos):
        if number == 4:
            Meteor([self.camera_group, self.meteor_group, self.harmful_group], pos, self.meteor_image, self.collision_group, self.player, self.music_effects)

    def _create_player(self, layout, tile_height, tile_width):
            for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_height
                            x = col_index *tile_width
                            return PlayerAmongUs([self.player_group, self.camera_group], (x, y), self.collision_group, self.harmful_group, self.ship_group, self.music_box)
        
    def _create_terrain(self, layout, type, tile_height, tile_width, image):
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        y = row_index *tile_height
                        x = col_index *tile_width 
                        if value != "-1":
                            
                            if type == "terrain":
                                StaticTile([self.collision_group, self.camera_group], (x, y), image[int(value)])
                               
                            if type == "boddies":
                                StaticTile([ self.camera_group], (x, y), image[int(value)])

                            if type == "spikes":
                                StaticTile([self.camera_group, self.harmful_group], (x, y), image[int(value)])
                            
                            if type == "volcano":

                                AnimatedTile([self.camera_group, self.animated_group, self.harmful_group], (x, y), image, self.player)

                            if type == "lava":
                                AnimatedTile([self.camera_group, self.animated_group, self.harmful_group], (x, y), image, self.player)

                            if type == "masks":
                                StaticTile([ self.camera_group], (x, y), image[int(value)])
                            
                            if type == "wires":
                                WireEnemy([self.camera_group, self.enemy_wires_group], (x,y), image, self.player, self.camera_group, self.harmful_group)

                            if type == "ship":
                                StaticTile([self.camera_group, self.ship_group], (x, y), image[int(value)])


class MainMenu:
    def __init__(self, level):
       
        self.surface = pygame.display.get_surface()
        self.image = pygame.image.load("Graphics/menu.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, screen)
        self.rect = self.image.get_rect(topleft = (0,0))
        self.start_button = Button("Graphics/start_button.png", (500, 100))
        self.mute_button = Button("Graphics/mute_intro.png", (500, 300))
        self.quit_button = Button("Graphics/quit.png", (500, 500))
        self.level = level

    def run(self):
        
        self.surface.fill("black")
        self.surface.blit(self.image, (0,0))
        self.start_button.draw()
        self.mute_button.draw()
        self.quit_button.draw()
 

    def check_game_state(self):
        if self.start_button.clicked:
            return "level_1"
        
        elif self.mute_button.clicked:
            self.level.play_intro = False
            self.level.intro_timer = 1321
            return "main_menu"

        elif self.quit_button.clicked:
            return "quit"
        else: return "main_menu"