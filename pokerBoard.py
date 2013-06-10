import playingCards
import time
import pygame, sys
from pygame.locals import *
from playingCards import *

locs = [300, 380, 460, 540, 620]
players = [400, 700, 100]
displayY = [500, 200]
displayX = [300, 300]


class GUI():
	def __init__(self, stackSize):
		pygame.init()
		self.fpsClock = pygame.time.Clock()
		self.windowSurfaceObj = pygame.display.set_mode((800, 800))
		pygame.display.set_caption('Heads Up Limit')

		#paint board background
		self.windowSurfaceObj.fill(green)

		#draw deck image
		backImage = pygame.image.load("cards/b.gif")
		for i in range(0, 10, 2):
			self.windowSurfaceObj.blit(backImage, (locs[0]-130-i, players[0]-50))
	
		#draw background on board for where cards will go
		for i in range(5):
			pygame.draw.circle(self.windowSurfaceObj, red, (locs[i], players[0]), 10, 0)

		self.updateTally(stackSize, stackSize, 0)

		#draw card outlines
		#for i in range(2):
		#	for j in range(2):
		#		pygame.draw.circle(windowSurfaceObj, red, (locs[i+1], players[j+1]), 10, 0)
	
	def update(self):
		showBoard = True
                pygame.display.update()
                self.fpsClock.tick(30)
                for event in pygame.event.get():
                        if event.type == QUIT:
                               	showBoard = False 
                        elif event.type == MOUSEMOTION:
                                mousex, mousey = event.pos
                        elif event.type == MOUSEBUTTONUP:
                                mousex, mousey = event.pos
                                if event.button == 1: #left click
                                        msg = 'left click'
		return showBoard

	def displayBackCard(self, locNum, player):
		backImage = pygame.image.load("cards/b.gif")
		self.windowSurfaceObj.blit(backImage, (locs[locNum] - 50, players[player] - 50))	

	def displayCard(self, player, locNum, hide, card):
		#player 0 = board
		#	1 = human
		#	2 = AI
		if not hide:
			card.displayCard(self.windowSurfaceObj, locs[locNum], players[player])
		else:
			self.displayBackCard(locNum, player)
		self.update()
		time.sleep(2)

	def updateTally(self, p1, p2, pot):
		#draw rect for keepying stack info
		self.windowSurfaceObj.fill(white, Rect(600, 0, 200, 100))
		font = pygame.font.Font(None, 25)
		textBox = font.render('pot:'+str(pot), False, (0, 0, 0))
		self.windowSurfaceObj.blit(textBox, (600, 0))
		textBox = font.render('AI:'+str(p2), False, (0, 0, 0))
		self.windowSurfaceObj.blit(textBox, (600, 35))
		textBox = font.render('human:'+str(p1), False, (0, 0, 0))
		self.windowSurfaceObj.blit(textBox, (600, 70))
		self.update()
	
	def displayMoves(self, player, canBet, canMove, callVal, betVal):
		black = (0, 0, 0)
		grey = (190, 190, 190)
		color = black
		if not canMove:
			fillColor = green
		else:
			fillColor = white
		self.windowSurfaceObj.fill(fillColor, Rect(displayX[player], displayY[player], 350, 150))
		
		if canMove:
			font = pygame.font.Font(None, 25)
			textBox = font.render('press the corresponding number to move', False, color)
			self.windowSurfaceObj.blit(textBox, (displayX[player], displayY[player]))
			textBox = font.render('[0] fold', False, color)
			self.windowSurfaceObj.blit(textBox, (displayX[player], displayY[player]+30))
			textBox = font.render('[1] call '+str(callVal), False, color)
			self.windowSurfaceObj.blit(textBox, (displayX[player], displayY[player]+60))
			if canMove and (not canBet):
				color = grey
			textBox = font.render('[2] bet '+str(betVal), False, color)
			self.windowSurfaceObj.blit(textBox, (displayX[player], displayY[player]+90))

	
	def getInput(self, actionTo, canBet, callVal, betVal):
		moved = False

		#display greyed out options for other player
		self.displayMoves(int(not actionTo), False, False, 0, 0)  
		
		#display options for current player
		self.displayMoves(actionTo, canBet, True, callVal, betVal)

		self.update()		

		#get input from keyboard
		while(not moved):
			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
					#keyinput = int(pygame.key.get_pressed())
					keypress = event.unicode
					if keypress == '0':
						nextMove = 0
						moved = True
					elif keypress == '1':
						nextMove = 1
						moved = True
					elif keypress == '2':
						if canBet:
							nextMove = 2
							moved = True
					else:
						print "other"
		return nextMove	


if __name__ == '__main__':
	deck = Deck()
	boardGUI = GUI(100)
	boardGUI.update()
	boardGUI.displayCard(1, 0, False, deck.nextCard())
	boardGUI.displayCard(2, 0, True, '')
	boardGUI.updateTally(100, 100, 10)
	nextMove = boardGUI.getInput(1, True, 1, 1)
	print nextMove
	showBoard = True
	while showBoard:
		showBoard = boardGUI.update()
	pygame.quit()
