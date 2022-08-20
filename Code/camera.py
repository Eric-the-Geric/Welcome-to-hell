import pygame

class Camera(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.offset= pygame.math.Vector2()
        self.surface = pygame.display.get_surface()
        self.h_width = self.surface.get_size()[0]//2
        self.h_height = self.surface.get_size()[1]//2

    # Normal camera
    def focus_target(self, target):
        self.offset.x = self.h_width - target.rect.centerx
        
    # camera kind of lags behind
    def cool_camera(self, target):
        self.offset.x += (target.rect.centerx - self.offset.x - self.h_width)/30

    def custom_draw(self, target):
        
        #self.focus_target(target)
        self.cool_camera(target)
        for sprite in self.sprites():
            offset_pos = (sprite.rect.topleft - self.offset)
            self.surface.blit(sprite.image, offset_pos)
            
            # offset_pos = (sprite.rect.topleft + self.offset)/10 --> this seems to scale everything down by a factor of 10
            

