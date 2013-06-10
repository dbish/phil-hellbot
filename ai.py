import playingCards
import handCalculations
import math
import random
from playingCards import *
from numpy import *
import poker
from poker import *
from handCalculations import *

numSimulations = 10

preFlopU = array([
	[49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[29, 52, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[30, 32, 56, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[31, 33, 35, 59, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[31, 33, 35, 37, 62, 0, 0, 0, 0, 0, 0, 0, 0],
	[31, 33, 35, 37, 39, 65, 0, 0, 0, 0, 0, 0, 0],
	[34, 34, 36, 38, 40, 42, 68, 0, 0, 0, 0, 0, 0],
	[36, 37, 38, 40, 42, 44, 46, 71, 0, 0, 0, 0, 0],
	[39, 40, 41, 41, 43, 45, 47, 49, 74, 0, 0, 0, 0],
	[42, 42, 43, 44, 45, 47, 49, 51, 53, 77, 0, 0, 0],
	[45, 46, 46, 47, 48, 49, 51, 53, 55, 56, 79, 0, 0],
	[48, 49, 50, 51, 52, 53, 54, 56, 58, 59, 60, 82, 0],
	[52, 53, 54, 55, 55, 57, 58, 59, 61, 62, 63, 64, 84]
	])
	 

preFlopS = array([
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[33.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[33.9, 35.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[34.9, 36.7, 38.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[34.8, 36.6, 38.4, 40.3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[35.4, 37.3, 39.1, 40.9, 42.8, 0, 0, 0, 0, 0, 0, 0, 0],
	[37.6, 38.2, 40.1, 41.9, 43.8, 45.6, 0, 0, 0, 0, 0, 0, 0],
	[39.9, 40.8, 41.4, 43.3, 45.1, 46.9, 48.8, 0, 0, 0, 0, 0, 0],
	[42.5, 43.3, 44.2, 44.9, 46.8, 48.6, 50.5, 52.3, 0, 0, 0, 0, 0],
	[45.2, 46.0, 46.8, 47.8, 48.5, 50.4, 52.3, 56.1, 56.1, 0, 0, 0, 0],
	[48.1, 48.9, 49.7, 50.7, 51.6, 52.5, 54.4, 56.2, 58.1, 59.0, 0, 0, 0],
	[51.2, 52.0, 52.8, 53.8, 54.8, 55.8, 56.7, 58.6, 60.5, 61.4, 62.4, 0, 0],
	[55.5, 56.3, 57.1, 58.0, 58.1, 59.3, 60.5, 61.5, 63.4, 64.3, 65.2, 66.2, 0]
	])

def simulate(hole, board, oType):
	deck = Deck()
	deck.shuffle()
	numKnown = len(board)
	oCards = []	
	found = False	

	#print len(hole)
	#print len(board)
	#take known cards out of simulation deck
	for card in (board+hole):
		deck.remove(card)
	#print deck.length()

	#choose cards for opponent
	if oType == 0:#loose player
		oCards.append(deck.nextCard())
		oCards.append(deck.nextCard())
	else:
		while not found:
			card1 = deck.nextCard()
			card2 = deck.nextCard()
			if card2.nameVal > card1.nameVal:
				temp = card1
				card1 = card2
				card2 = temp 

			if card1.suitVal == card2.suitVal:
				wOdds = float(preFlopS[card1.nameVal][card2.nameVal])
			else:
				wOdds = float(preFlopU[card1.nameVal][card2.nameVal])
			if wOdds > 50:
				oCards.append(card1)
				oCards.append(card2)
				found = True
			else:
				deck.cards.insert(0, card1)
				deck.cards.insert(0, card2)
			

	#simulated board
	sBoard = board[:]
	#choose the rest of board cards
	for i in range(5-len(board)):
		sBoard.append(deck.nextCard())
	
	#decide who won
	best = bestHand(hole+sBoard)
	oBest = bestHand(oCards+sBoard)
	winner = compareHands(best, oBest)
	if winner:
		return 1
	else:
		return 0

class AI():
	def __init__(self, playerState, brainType):
		self.playerState = playerState
		if brainType == 1:
			self.chooseMove = self.chooseMove_m
		elif brainType == 0:
			self.chooseMove = self.chooseMove_random
		elif brainType == 2:
			self.chooseMove = self.chooseMove_cons
		elif brainType == 3:
			self.chooseMove = self.chooseMove_loose
		

	def chooseMove_m(self, boardCards, pot, callAmount, betAmount, canBet, oStyle):
		pOdds = float(callAmount/(float(pot+callAmount)))

		#print pOdds
		if not oStyle:#loose player, adjust odds accordingly
			pOdds = float((callAmount+4*betAmount)/(float(pot+callAmount+4*betAmount))) 
			#print pOdds
		#print pOdds
		#print "###"
			

		cards = self.playerState.holeCards
		ipOdds = float(betAmount/(float(pot+betAmount)))

		#print "t ",
		#print len(boardCards)	
		#pre-flop odds lookup
		if len(boardCards) == 0:
			if cards[1].nameVal > cards[0].nameVal:
				temp = cards[0]
				cards[0] = cards[1]
				cards[1] = temp

			if cards[0].suitVal == cards[1].suitVal:
				wOdds = float(preFlopS[cards[0].nameVal][cards[1].nameVal]/float(100))
			else:
				wOdds = float(preFlopU[cards[0].nameVal][cards[1].nameVal]/float(100))
				pOdds = .5
				iOdds = .6
		else:
			#basic Monte-carlo simulation
			numWins = 0
			for i in range(numSimulations):
				numWins = numWins + simulate(cards, boardCards, oStyle)
			if numWins == 0:
				wOdds = 0  
			else:
				wOdds = float(numWins/float(numSimulations))
		#print "pot odds:"+str(pOdds)
		#print "odds of winning:"+str(wOdds)
		#print "implied pot odds:"+str(ipOdds)

		
		if wOdds > pOdds:
			if wOdds > ipOdds: #raise
				move = 2
			else: #call
				move = 1
		else: #bad odds, fold
			move = 0
		
		if (not canBet) and (move == 2):
			move = 1		
		
		if (move == 0) and (callAmount == 0): #check if you can
			move = 1

		return move

	def chooseMove_random(self, boardCards, pot, callAmount, betAmount, canBet, oStyle):
		move = random.randint(0, 3)
		if (not canBet) and (move == 2):
			move = 1
		elif (move == 0) and (callAmount == 0):
			move = 1
		return move


	# this is a player that likes to play all hands as long as he a decent
	# set of hole cards
	def chooseMove_loose(self, boardCards, pot, callAmount, betAmount, canBet, oStyle):
		cards = self.playerState.holeCards
		move = 2 #default = raise
		
		if len(boardCards) == 0:
			if cards[1].nameVal > cards[0].nameVal:
				temp = cards[0]
				cards[0] = cards[1]
				cards[1] = temp

			if cards[0].suitVal == cards[1].suitVal:
				wOdds = float(preFlopS[cards[0].nameVal][cards[1].nameVal]/float(100))
			else:
				wOdds = float(preFlopU[cards[0].nameVal][cards[1].nameVal]/float(100))
			if wOdds < .35:
				move = 0
		
		if (not canBet) and (move == 2):
			move = 1
		if (move == 0) and (callAmount == 0): #check if you can
			move = 1
		
		return move

	#this is a basic very conservative player
	#moves will only be made with very good starting cards
	#and after the flop having a hand of top pair or better
	def chooseMove_cons(self, boardCards, pot, callAmount, betAmount, canBet, oStyle):
		cards = self.playerState.holeCards
		move = 0 #default is to fold

		#only play pre-flop if odds are better then 60%
		if len(boardCards) == 0:
			if cards[1].nameVal > cards[0].nameVal:
				temp = cards[0]
				cards[0] = cards[1]
				cards[1] = temp
			if cards[0].suitVal == cards[1].suitVal:
				wOdds = float(preFlopS[cards[0].nameVal][cards[1].nameVal]/float(100))
			else:
				wOdds = float(preFlopU[cards[0].nameVal][cards[1].nameVal]/float(100))
			if wOdds > .6:
				move = 2
		else:
			#determine what the top pair would be
			topHandCard = bestCard(cards)
			topCard = bestCard(boardCards+cards)

			if len(boardCards) == 3:
				best5 = boardCards + cards
			elif len(boardCards) == 4:
				best5 = bestHand6(boardCards + cards)
			else:
				best5 = bestHand(boardCards + cards)
				
			#only play if the hand is better then the top pair
			if handEval(handValue(best5)) <= 6185: #pair or better
				if handEval(handValue(best5)) > 3325: #just one pair
					if topHandCard.nameVal == topCard.nameVal: #holds the best pair
						move = 2 
				else:#better then a pair
					move = 2

		if (not canBet) and (move == 2):
			move = 1
		if (move == 0) and (callAmount == 0): #check if you can
			move = 1

		return move
		
		
	
if __name__ == '__main__':
	player = Player(100)
	brain = AI(player, 0)
	player.holeCards.append(Card(1, 12))
	player.holeCards.append(Card(0, 11))
	board = []
	#test pre-flop lookup
	move = brain.chooseMove(board, 6, 2, 4)
	print "Move chosen: ",
	print move
	board.append(Card(1, 1))
	board.append(Card(2,3))
	board.append(Card(0, 7))
	move = brain.chooseMove(board, 6, 2, 4)
	print "Move chosen: ",
	print move
	
