import pygame
from Ball import *
from pygame.locals import *
import random
import pygame.time
import sys

class Particle_physics():

	def __init__(self):
		pygame.init()
		pygame.display.init()
		self.clock = pygame.time.Clock()
		self.display = pygame.display.set_mode((800,600))

	def run(self):	
		ballgroup = pygame.sprite.Group()
		for now in range(10):
			now = Ball((0,0,0), 100)
			ballgroup.add(now)
		while True:
			self.clock.tick(60)
			self.display.fill((255,255,255))
			event = pygame.event.get()
			for e in event:
				if e.type == QUIT:
					pygame.quit(); sys.exit(0);
				elif e.type == KEYDOWN:
					if e.key == K_ESCAPE:
						pygame.quit(); sys.exit(0);
					if e.key == K_SPACE:
						for now in range(10):
							now = Ball((0,0,0), 100)
							ballgroup.add(now)
			ballgroup.draw(self.display)
			if ballgroup is not None:	
				self.updateballs(ballgroup)
			pygame.display.flip()

	
	def updateballs(self, spritegroup):
		for balls in spritegroup:
			result = balls.update()
			if result == 1:
				spritegroup.remove(balls)
	
if __name__ == '__main__':
	program = Particle_physics()
	program.run()

