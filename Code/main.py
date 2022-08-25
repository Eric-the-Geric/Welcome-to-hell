
#################################################################
# Idea's for the game:
# Figure out what the main mechanic should be
# add death counter
# Change all the graphics xD
# make a level selector
# Make some more levels
# Add particles
# Add sounds
# add enemies
#################################################################


import pygame, sys
from settings import *
from helper import *
from level import Level_0, MainMenu, Level_selector, Level_1

def main():
    # Initialize pygame
    pygame.init()

    # Constant variables
    surface = pygame.display.set_mode(screen)
    pygame.display.set_caption('Kinda sus')
    clock = pygame.time.Clock()

    #Boolean for while loop
    run = True

    # Initialize main menu
    menu = MainMenu()
    
    # Initialize level
    #level0 = Level_0()
    level1 = Level_1()

    # Initialize level selector
    level_selector = Level_selector()

    game_state = "main_menu"
    while run:
        surface.fill('black')
        
        if game_state == "level_1":
            # level0.run()
            level1.run()

        elif game_state == "main_menu":
            menu.run()

            game_state = menu.check_game_state()

        elif game_state == "level_selection":
            level_selector.run()
            game_state = level_selector.check_game_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = "main_menu"
                
        pygame.display.update()
        clock.tick(FPS)
        

if __name__ == '__main__':
    main()