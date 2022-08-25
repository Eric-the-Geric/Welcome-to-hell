import pygame
from helper import *
from settings import *
from level_data import *
from tile import *
from player import Player, PlayerAmongUs
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

        self.Level_1 = {"Background": "Map/Level_1_Background.csv",
            "Clouds": "Map/Level_1_Clouds.csv",
            "Player": "Map/Level_1_Player.csv",
            "Stars": "Map/Level_1_Stars.csv",
            "Terrain": "Map/Level_1_Terrain.csv"}
        
        # Getting the layout data
        self.player_layout = import_map_data(self.Level_1["Player"])
        self.cloud_layout = import_map_data(self.Level_1["Clouds"])
        self.terrain_layout = import_map_data(self.Level_1["Terrain"])
        self.stars_layout = import_map_data(self.Level_1["Stars"])
        self.background_layout = import_map_data(self.Level_1["Background"])

        
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
            self.player.rect.topleft = (10*tile_size, 11*tile_size)
            
    
    def _create_player(self, layout):
            for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_size
                            x = col_index *tile_size
                    
                            return Player([self.player_group, self.camera_group], (x,y), self.collision_group)
        
    def _create_terrain(self, layout, type):
        if type == "background":
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        if value != "-1":
                            y = row_index *tile_size
                            x = col_index *tile_size
                            if value == "0":
                                Background([self.visible_group, self.camera_group], (x, y))
        if type == "terrain":
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        if value != "-1":
                            y = row_index *tile_size
                            x = col_index *tile_size
                            
                            if value == "3":
                                TerrainTile2([self.visible_group, self.collision_group, self.camera_group], (x, y))

                            elif value == "2":

                                TerrainTile1([self.visible_group, self.collision_group, self.camera_group], (x, y))
        if type == "cloud":
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        if value != "-1":
                            y = row_index *tile_size
                            x = col_index *tile_size
                            if value == "4":
                                Clouds1([self.visible_group, self.camera_group, self.collision_group], (x, y))
                            elif value == "5":
                                Clouds2([self.visible_group, self.camera_group, self.collision_group], (x, y))
        if type == "star":
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        if value != "-1":
                            y = row_index *tile_size
                            x = col_index *tile_size
                            if value == "1":
                                Stars([self.visible_group, self.camera_group], (x, y))

class Level_1:

    def __init__(self):
        # Get the surface
        self.surface = pygame.display.get_surface()

        # Setting up sprite groups
        self.player_group = pygame.sprite.GroupSingle()
        self.visible_group = pygame.sprite.Group()
        self.collision_group = pygame.sprite.Group()
        self.animated_group = pygame.sprite.Group()
        self.camera_group = Camera()
        self.harmful_group = pygame.sprite.Group()

        # Getting the layout data
        self.player_layout = import_map_data(Level_2["Player"])
        self.lava_layout = import_map_data(Level_2["Lava"])
        self.terrain_layout = import_map_data(Level_2["Terrain"])
        self.spikes_layout = import_map_data(Level_2["Spikes"])
        self.volcano_layout = import_map_data(Level_2["Volcano"])
        self.boddies_layout = import_map_data(Level_2["Boddies"])

        # Setting up images
        
        self.lava_image = import_complicated_full_sprite_sheet("Graphics2/lava block.png",
                                                            32, 32, (255,127,39))
        self.terrain_image = import_complicated_full_sprite_sheet("Graphics2/grass.png",
                                                            32, 32, (255,127,39))
        self.spikes_image = import_complicated_full_sprite_sheet("Graphics2/rockspikes.png",
                                                            81, 63, (255,127,39))
        self.volcano_image = import_complicated_full_sprite_sheet("Graphics2/volcano.png",
                                                            110, 52, (255,127,39))
        self.boddies_image = import_complicated_full_sprite_sheet("Graphics2/dead.png",
                                                            31, 34, (255,127,39))                                                        

                                    
        # Setting up map sprites
        
        self.spikes =  self._create_terrain(self.spikes_layout, "spikes", 32, 32, self.spikes_image)
        
        self.volcano =  self._create_terrain(self.volcano_layout, "volcano", 32, 32, self.volcano_image)
        
        self.terrain = self._create_terrain(self.terrain_layout, "terrain", 32, 32, self.terrain_image)

        self.boddies =  self._create_terrain(self.boddies_layout, "boddies", 32, 32, self.boddies_image)
        
        # Setting up player sprite
        self.player = self._create_player(self.player_layout, 48, 36)

        # Lava later so it renders over the player
        self.lava = self._create_terrain(self.lava_layout, "lava", 32, 32, self.lava_image)

        
        
    def run(self):
        self.animated_group.update()
        self.camera_group.custom_draw(self.player)
        #self.visible_group.draw(self.surface)
        self.player_group.update()
        
    
    def _create_player(self, layout, tile_height, tile_width):
            for row_index, row in enumerate(layout):
                for col_index, value in enumerate(row):
                    if value != '-1':
                        if value == '0':
                            y = row_index *tile_height
                            x = col_index *tile_width
                            return PlayerAmongUs([self.player_group, self.camera_group], (x, y), self.collision_group, self.harmful_group)
        
    def _create_terrain(self, layout, type, tile_height, tile_width, image):
            for row_index, row in enumerate(layout):
                    for col_index, value in enumerate(row):
                        y = row_index *tile_height
                        x = col_index *tile_width 
                        if value != "-1":
                            
                            if type == "terrain":
                                StaticTile([self.visible_group, self.collision_group, self.camera_group], (x, y), image[int(value)])
                               
                            if type == "boddies":
                                StaticTile([self.visible_group,  self.camera_group], (x, y), image[int(value)])

                            if type == "spikes":
                                StaticTile([self.visible_group, self.camera_group, self.harmful_group], (x, y), image[int(value)])
                            
                            if type == "volcano":

                                AnimatedTile([self.visible_group, self.camera_group, self.animated_group, self.harmful_group], (x, y), image)


                            if type == "lava":
                                 AnimatedTile([self.visible_group, self.camera_group, self.animated_group, self.harmful_group], (x, y), image)
                        


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
        # self.image = pygame.image.load("Graphics/level_0.png").convert_alpha()
        # self.image = pygame.transform.scale(self.image, (400, 200))
        # self.rect = self.image.get_rect(topleft = (0,0))
        self.start_button = Button("Graphics/Level_0.png", (400, 250))
        
    def run(self):
        self.surface.fill("black")
        
        self.start_button.draw()
    
    def check_game_state(self):
        if self.start_button.clicked:
            return "level_1"
        
        else: return "level_selection"