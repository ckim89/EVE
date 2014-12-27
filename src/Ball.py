import pygame
import random
import time


class Ball(pygame.sprite.DirtySprite):
    def __init__(self, color, rad, pos, im = None):
        pygame.sprite.DirtySprite.__init__(self)
        self.size = random.randint(4, 10)
        if im == None:
            self.image = pygame.surface.Surface((self.size, self.size))
            if color == (0, 0, 0):
                self.image.fill((random.randint(180, 220), 0, 0))
            else:
                self.image.fill((255, 0, 0))
            self.xvel = random.randint(-10, 10)
            self.yvel = round(random.uniform(1, 6.999), 3)
            self.offy = round(random.uniform(.200, .300), 3)
            self.offx = round(random.uniform(.9, 1.0), 1)
            self.threshold = 0.4
        else:
            self.image = im
            self.xvel = random.randint(-4, 4)
            self.yvel = round(random.uniform(0.5, 1), 3)
            self.offy = round(random.uniform(.200, .300), 3)
            self.offx = round(random.uniform(.9, 1.0), 1)
            self.threshold = 0.7

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dirty = 2

        self.count = 1.5
        self.startime = time.time()

    def update(self):
        self.dirty = 1
        self.gravity()
        self.rect = self.rect.move(self.xvel, self.yvel)
        if self.image.get_size() == (100, 100):
            self.count += .2
        else:
            self.count += 0.5
        if time.time() - self.startime >= self.threshold:
            del self
            return 1
        else:
            return 0

    def gravity(self):
        self.xvel = self.offx * self.xvel
        self.yvel = self.offy * self.count**2
        offset = -2 * self.count
        self.yvel = self.yvel + offset

    def __del__(self):
        pass
