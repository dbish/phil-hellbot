import pygame, sys, random
from pygame.locals import *

suits = ['d', 's', 'h', 'c']
names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
green = pygame.Color(0, 255, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)

class Card():
	def __init__(self, suitVal, nameVal):
		self.suitVal = suitVal
		self.nameVal = nameVal

	def suit(self):
		return suits[self.suitVal]

	def name(self):
		return names[self.nameVal]

	def displayCard(self, surface, x, y):
		cardName = self.name() + self.suit() + ".gif"
		cardImage = pygame.image.load("cards/"+cardName)
		surface.blit(cardImage, (x-50, y-50))	

	def __str__(self):
		return "%s%s" % (self.name(), self.suit())

class Deck():
	def __init__(self):
		self.cards = []
		for suit in range(len(suits)):
			for name in range(len(names)):
				self.cards.append(Card(suit, name))	
	
	#random shuffle uses the Knuth algo
	def shuffle(self):
		random.shuffle(self.cards)

	def nextCard(self):
		return self.cards.pop()	

	def getCards(self):
		return self.cards

	def remove(self, c):
		for card in self.cards:
			if (card.suitVal == c.suitVal) and (card.nameVal == c.nameVal):
				self.cards.remove(card)

	def length(self):
		return len(self.cards)

if __name__ == '__main__':
	deck = Deck()
	deck.shuffle()
	for i in range(51):
		print deck.nextCard() 
	print len(deck.getCards())	

	pygame.init()
	fpsClock = pygame.time.Clock()

	#display board
	windowSurfaceObj = pygame.display.set_mode((200, 200))
	pygame.display.set_caption('Test!')
	
	while True:

		windowSurfaceObj.fill(white)

		
		deck.getCards()[0].displayCard(windowSurfaceObj, 100, 100)

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
