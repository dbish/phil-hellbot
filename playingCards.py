import pygame
from pygame.locals import *

suits = ['diamond', 'spade', 'heart', 'club']
names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
green = pygame.Color(0, 255, 0)
white = pygame.Color(255, 255, 255)

class Card():
	def __init__(self, suitVal, nameVal):
		self.suitVal = suitVal
		self.nameVal = nameVal

	def suit(self):
		return suits[self.suitVal]

	def name(self):
		return names[self.nameVal]

	#def displayCard(x, y, hide=False):
		

	def __str__(self):
		return "%s of %ss" % (self.name(), self.suit())

class Deck():
	def __init__(self):
		self.cards = []
		for suit in range(len(suits)):
			for name in range(len(names)):
				self.cards.append(Card(suit, name))	

	def getCards(self):
		return self.cards

if __name__ == '__main__':
	deck = Deck()
	for card in deck.getCards():
		print card
	
	pygame.init()
	fpsClock = pygame.time.Clock()

	#display board
	windowSurfaceObj = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('Heads Up!')
	
	while True:
		windowSurfaceObj.fill(green)
		
		#draw card outlines
		pygame.draw.rect(windowSurfaceObj, white, (10, 10, 50, 100))
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				if event.button == 1: #left click
					msg = 'left click'
	
		pygame.display.update()
		fpsClock.tick(30)
