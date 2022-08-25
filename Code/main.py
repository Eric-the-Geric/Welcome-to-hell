
#################################################################
# Idea's for the game:
# add death counter
# Add particles
# Add sounds
# add enemies (electrical enemy)
# Add secret easter egg which will just be me saying there is no easter egg (to the left of the level)
# finish the actual level
# Make this main file into a class with the different game loops
# add some kind of ending I guess
# add death counter
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