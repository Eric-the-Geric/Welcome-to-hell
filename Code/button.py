import pygame



class Button():
    def __init__(self, path, pos):

        self.surface = pygame.display.get_surface()
        self.image = pygame.image.load(path).convert_alpha()
        self.image.set_alpha(150)
        self.image = pygame.transform.scale(self.image, (300, 150))
        self.rect = self.image.get_rect(center = pos)
        self.clicked = False
        self.pos = pos


    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.image.set_alpha(255)
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
        else:
            self.image.set_alpha(150)
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        

        self.surface.blit(self.image, self.pos)