import pygame
from helper import *
from settings import *
from level_data import *
from tile import *
from player import Player
from camera import *
from button import *



class Level_0:
    
    def __init__(self):
        # Get the surface
        self.surface = pygame.display.get_surface()

        # Setting up sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.visible_group = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        self.camera_group = Camera()
        # Getting the layout data
        self.player_layout = import_map_data(Level_1["Player"])
        self.cloud_layout = import_map_data(Level_1["Clouds"])
        self.terrain_layout = import_map_data(Level_1["Terrain"])
        self.stars_layout = import_map_data(Level_1["Stars"])
        self.background_layout = import_map_data(Level_1["Background"])

        
        # Setting up map sprites
        self.background = self._create_terrain(self.background_layout, "background")
        self.stars = self._create_terrain(self.stars_layout, "star")
        self.clouds = self._create_terrain(self.cloud_layout, "cloud")
        self.terrain = self._create_terrain(self.terrain_layout, "terrain")

        # Setting up player sprite
        self.player = self._create_player(self.player_layout)
        
    def run(self):
        self.camera_group.custom_draw(self.player)
        self.player_group.update()
        if self.player.rect.centery > screen_height*2:
            self.player.rect.topleft = (10*tile_size*scaling_factor, 11*tile_size*scaling_factor)
            
    
    def _create_player(self, layout):
            for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size*scaling_factor
                            x = col_index *tile_size*scaling_factor
                    
                            return Player([self.player_group, self.camera_group], (x,y), self.collision_group)
        
    def _create_terrain(self, layout, type):
        if type == "background":
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        if value != "-1":
                            y = row_index *tile_size*scaling_factor
                            x = col_index *tile_size*scaling_factor
                            if value == "0":
                                Background([self.visible_group, self.camera_group], (x, y))
        if type == "terrain":
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        if value != "-1":
                            y = row_index *tile_size*scaling_factor
                            x = col_index *tile_size*scaling_factor
                            
                            if value == "3":
                                TerrainTile2([self.visible_group, self.collision_group, self.camera_group], (x, y))

                            elif value == "2":

                                TerrainTile1([self.visible_group, self.collision_group, self.camera_group], (x, y))
        if type == "cloud":
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        if value != "-1":
                            y = row_index *tile_size*scaling_factor
                            x = col_index *tile_size*scaling_factor
                            if value == "4":
                                Clouds1([self.visible_group, self.camera_group, self.collision_group], (x, y))
                            elif value == "5":
                                Clouds2([self.visible_group, self.camera_group, self.collision_group], (x, y))
        if type == "star":
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        if value != "-1":
                            y = row_index *tile_size*scaling_factor
                            x = col_index *tile_size*scaling_factor
                            if value == "1":
                                Stars([self.visible_group, self.camera_group], (x, y))

class MainMenu:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.image = pygame.image.load("Graphics/menu.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, screen)
        self.rect = self.image.get_rect(topleft = (0,0))
        self.start_button = Button("Graphics/start_button.png", (500, screen_height//1.5))
        self.level_button = Button("Graphics/levels.png", (500, screen_height//2))
    def run(self):
        self.surface.fill("black")
        self.surface.blit(self.image, (0,0))
        self.start_button.draw()
        self.level_button.draw()
        
        

    def check_game_state(self):
        if self.start_button.clicked:
            return "level_1"
        elif self.level_button.clicked:
            return "level_selection"
        else: return "main_menu"

class Level_selector:
    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.image = pygame.image.load("Graphics/level_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, screen)
        self.rect = self.image.get_rect(topleft = (0,0))
        self.start_button = Button("Graphics/start_button.png", (750, 300))
        
    def run(self):
        self.surface.fill("black")
        self.surface.blit(self.image, (0,0))
        self.start_button.draw()
    
    def check_game_state(self):
        if self.start_button.clicked:
            return "level_1"
        
        else: return "level_selection"