import pygame
class Door(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self)
        self.location = location


    def teleport_hax(self, player_location):
        if player_location.collidepoint(self.location):
            return (200,0)
        return (0,0)
