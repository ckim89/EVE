import pygame
import sys

#TODO: Rewrite each game state to fit the following structure:
#All gamestate have a background and a some sort of track playing
#So parent class will have a background, basic track and some basic
#control methods for each (that will most liekly be overriden)
#These parent class will be called in each method override

#The update method for each subclass will be overriden. The only constant
#is the background and music background track

#Things to maybe consider:
#	- Background layering control for parent class? (e.g. tree rendered over character, character rendered over level)
#	- 

class GAME_STATES(object):
	def __init__(self):
		#TODO Set background member var and add it to update method
		self.DRAW_DISP = pygame.display.get_surface()
		
	def update(self,event):
		pass
	

	def draw_display(self):
		pass
			
			
