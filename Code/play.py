
#################################################################
# Make this main file into a class with the different game loops
#################################################################


import pygame, sys
from settings import *
from helper import *
from level import MainMenu, Level_1
from sound_effects import SoundEffects

def display_fps(clock, level1, offset, surface, font):
        text = font.render("FPS: " + str(int(clock.get_fps())), True, ("white"))
        textRect = text.get_rect()
        offset.x += (level1.player.rect.centerx - 540 - offset.x - (screen_width//2))
        offset.y += (level1.player.rect.centery + 300 - offset.y - (screen_height)//2)
        textRect.center = (level1.player.rect.topleft - offset)
        surface.blit(text, textRect)

def main():
    music_box = SoundEffects()
    # Initialize pygame
    pygame.init()
    # Constant variables
    surface = pygame.display.set_mode(screen)
    pygame.display.set_caption('Kinda sus')
    clock = pygame.time.Clock()
    #Boolean for while loop
    run = True

    # Initialize main menu
    
    
    # Initialize level
    level1 = Level_1(music_box)
    menu = MainMenu(level1)
    bg1 = pygame.image.load("Graphics2/BackgroundL1.png").convert()
    bg2 = pygame.image.load("Graphics2/BackgroundL2.png").convert()
    bg1.set_colorkey((255,127,39))
    bg2.set_colorkey((255,127,39))
    scroll1 = [0, 0]
    scroll2 = [0, 0]
    offset = pygame.math.Vector2()
    font = pygame.font.Font(None, 36)

    game_state = "main_menu"
    music_box.play_song("menu", 0.1)
    while run:
        # WAYYYYYYYY better to get the event list and loop over that list multiple times per frame than call the event listener each time.
        # It fixed the issue with my jumping
        events = pygame.event.get()

        scroll1[0] =  (level1.player.rect.centerx-5000- scroll1[0])/20
        scroll1[1] =  (level1.player.rect.centery-5000- scroll1[1])/20
        scroll2[0] = (level1.player.rect.centerx-5000- scroll2[0])/200
        scroll2[1] = (level1.player.rect.centery-5000 -scroll2[1])/200
        surface.fill('black')
        
        surface.blit(bg1, (scroll1[0],scroll1[1]))
        surface.blit(bg2, (scroll2[0],scroll2[1]))
        
        
        if game_state == "level_1":
            
            level1.run(events)
            

        elif game_state == "main_menu":
            menu.run()
            game_state = menu.check_game_state()
            

        elif game_state == "main_menu2":
            menu.run()
            game_state = menu.check_game_state()

        elif game_state == "quit":
            run = False
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu.image.set_alpha(50)
                    game_state = "main_menu2"
                    

                
        display_fps(clock, level1, offset, surface, font)
        pygame.display.update()
        clock.tick(FPS)
 
if __name__ == '__main__':
    main()