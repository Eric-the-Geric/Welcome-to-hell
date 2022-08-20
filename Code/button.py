import pygame



class Button():
    def __init__(self, path, pos):

        self.surface = pygame.display.get_surface()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (300, 150))
        self.rect = self.image.get_rect(center = pos)
        self.clicked = False
        self.pos = pos


    def draw(self):
        action = False
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.clicked ==False:
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.surface.blit(self.image, self.pos)