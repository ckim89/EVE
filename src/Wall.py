import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../images/TILE_WALL.jpg')
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.name = 'wall'


