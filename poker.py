import playingCards
import pokerBoard
import math
import ai
import handCalculations
from playingCards import *
from pokerBoard import *
from handCalculations import *
from ai import *

name = ["C-3PO", "Guest"]
startingStack = 100
smallBet = 2
bigBet = 4
smallBlind = .5*smallBet
bigBlind = smallBet
#number of raises allowed before raises are capped
cap = 4

class Player():
	def __init__(self, stack, botType):
		self.holeCards = []
		self.hand = []
		self.stack = stack
		self.bet = 0 	
		if botType > -1:
			self.isHuman = False
		else:
			self.isHuman = True
		self.brain = AI(self, botType)

	def updateStack(self, delta):
		self.stack = self.stack + delta
		if self.stack < 0:
			delta = delta - self.stack
			self.stack = 0
			#print "Delta: "+str(delta)
		return -delta
			
	

class PokerGame():
	def __init__(self, g, bot, guest, v):
		#initialize game
		self.deck = Deck()
		self.players = []
		self.players.append(Player(startingStack, bot))
		self.players.append(Player(startingStack, guest))
		self.boardCards = [] 	
		self.gui = g
		self.button = 0
		self.pot = 0
		self.maxBet = 0
		self.textMoneyState()		
		self.v = v
		self.opponentPlayed = 0
		self.numHands = 0
		self.oStyle = 1

		#initialize graphics
		if g:
			self.boardGUI = GUI(startingStack)
			self.boardGUI.update()
		
	
	def updatePot(self, delta):
		if delta:
			self.pot = self.pot + delta
			if self.v:
				print "Pot now $"+str(self.pot)	
			

	def textBoardState(self):
		if len(self.boardCards):
			print "Board:"+"(",
			for card in self.boardCards:
				print str(card),
			print ")"		

	def textMoneyState(self):
		cStack = "C-3PO=$"+str(self.players[0].stack)
		gStack = "Guest=$"+str(self.players[1].stack)
		print "Stack size:(" + cStack+","+gStack+")" 		

	def dealStreet(self, sn):
		if not sn:
			#deal hole cards
			for i in range(2):
				for j in range(2):
					newCard = self.deck.nextCard()
					self.players[j].holeCards.append(newCard)
					if self.gui:
						self.boardGUI.displayCard(j+1, i, False, newCard)
			cards = self.players[1].holeCards
			if self.v:
				print "Deal to Guest:("+str(cards[0])+","+str(cards[1])+")"
		elif sn == 1:
			#deal flop (3 cards)
			for i in range(3):
				newCard = self.deck.nextCard()
				self.boardCards.append(newCard)
				if self.gui:
					self.boardGUI.displayCard(0, i, False, newCard)
		elif sn == 2:
			#deal turn (1 card)
			newCard = self.deck.nextCard()
			self.boardCards.append(newCard)
			if self.gui:
				self.boardGUI.displayCard(0, 3, False, newCard)
		else:
			#deal river (1 card)			
			newCard = self.deck.nextCard()
			self.boardCards.append(newCard)
			if self.gui:
				self.boardGUI.displayCard(0, 4, False, newCard)
		if not self.gui and self.v:
			self.textBoardState()
		
	def textInput(self, actionTo, canBet, callVal, betVal):
		moved = False
		
		while not moved:
			#display options
			print '[0] fold'
			print '[1] call ' + str(callVal)
			if canBet:
				print '[2] bet ' + str(betVal)
			move = input('choose a number :') 
			try:
				val = int(move)
				if val == 0 or val == 1:
					moved = True
				elif val == 2 and canBet:
					moved = True
			except ValueError:
				print 'that is not an allowed input'
		
		return val			


	def playStreet(self, street):
		if street:
			self.maxBet = 0
			raiseAmount = bigBet
		else:
			raiseAmount = smallBet
			self.numHands = self.numHands + 1

		if (not self.button):
			if (street == 0):
				self.numHands = self.numHands + 1	
				#if the opponent is playing a lot of hands he's loose, if not conservative
				if self.numHands > 5:
					if (float(self.opponentPlayed)/float(self.numHands-1)) > .1:
						self.oStyle = 1
					else:
						self.oStyle = 0		
					#print(float(self.opponentPlayed)/float(self.numHands))
			if (street == 1):
				self.opponentPlayed = self.opponentPlayed + 1 
		fold = -1	
		self.dealStreet(street)
		
		numChecks = 0
		numBets = 0
		callOccurred = False
		numMoves = 0
		actionTo = int(not self.button)		
		#nextMove: 0 = Fold, 1 = call, 2 = bet
		nextMove = 1

		while (numChecks < 2) and not (callOccurred and (numMoves > 1)) and nextMove:
			callOccurred = False
			if (numBets >= cap):
				canBet = False
			else:
				canBet = True

			callVal = self.maxBet - self.players[actionTo].bet
			betVal = self.maxBet + raiseAmount - self.players[actionTo].bet
			if betVal > self.players[actionTo].stack:
				betVal = self.players[actionTo].stack
			if betVal > self.players[int(not actionTo)].stack:
				betVal = self.players[int(not actionTo)].stack
			if not betVal:
				canBet = False
			if self.players[actionTo].isHuman: 
				if self.gui:
					nextMove = self.boardGUI.getInput(actionTo, canBet, callVal, betVal)
				else:
					nextMove = self.textInput(actionTo, canBet, callVal, betVal)
			else:
				nextMove = self.players[actionTo].brain.chooseMove(self.boardCards, self.pot, callVal, betVal, canBet, self.oStyle) 
			if nextMove > 0:
				if nextMove == 1: #call
					potDelta = callVal = self.players[actionTo].updateStack(-callVal) 
					if callVal:
						if self.v:
							print name[actionTo]+" calls $"+str(callVal)
					else:
						if self.v:
							print name[actionTo]+" checks"
					delta = callVal
					if delta == 0:
						numChecks = numChecks + 1
					callOccurred = True
				else: #raise
					potDelta = betVal = self.players[actionTo].updateStack(-betVal) 
					if self.v:
						print name[actionTo]+" bets $"+str(betVal)
					numBets = numBets + 1
					self.players[actionTo].bet = self.players[actionTo].bet + betVal 
					if self.players[actionTo].bet > self.maxBet:
						self.maxBet = self.players[actionTo].bet
				#update the pot and player's stack
				self.updatePot(potDelta)
				if self.v:
					self.textMoneyState()
			else:
				if self.v:
					print name[actionTo]+" folds"
				fold = actionTo 
			actionTo = int(not actionTo)
			numMoves = numMoves + 1
			

		stack1 = self.players[0].stack
		stack2 = self.players[1].stack
		self.players[0].bet = 0
		self.players[1].bet = 0
		if self.gui:
			self.boardGUI.updateTally(stack1, stack2, self.pot)
		return fold

	def updateButton(self):
		self.button = int(not self.button)

	def takeBlinds(self):
		if self.v:
			print "Dealing hand and taking blinds..."	
		self.pot = self.pot + self.players[int(not self.button)].updateStack(-smallBlind)
		self.updatePot(self.players[self.button].updateStack(-bigBlind))
		self.players[self.button].bet = bigBlind - smallBlind
		self.maxBet = bigBlind - smallBlind	
		if self.v:
			self.textMoneyState()

	def showCards(self, i, holeCards, bestHand):
		print name[i]+" has (",
		for card in holeCards:
			print card,
		print ")"
		print "best hand is (",
		for card in bestHand:
			print card,
		print ") ",
		print handRank(handEval(handValue(bestHand)))

	def playHand(self):
		self.deck = Deck()
		self.deck.shuffle()	
		self.takeBlinds()
		street = 0
		fold = -1 
		best = []
		botWins = 0
		while (fold == -1) and (street < 4):
			fold = self.playStreet(street)
			street = street+1
		if fold < 0:	
			#check for winner
			for i in range(2):
				best.append(bestHand(self.players[i].holeCards+self.boardCards))	
				if self.v:
					self.showCards(i, self.players[i].holeCards, best[i])
			winner = compareHands(best[0], best[1])
		else:
			winner = int(not fold)
		#give pot to winner
		if winner > -1:
			if self.v:
				print name[winner]+" wins $"+str(self.pot)
			if not winner:
				botWins = 1
		else:
			if self.v:
				print "tie..."

		if winner > -1:
			self.players[winner].updateStack(self.pot)
		else:
			splitPot = int(self.pot/2)
			self.players[0].updateStack(splitPot)
			self.players[1].updateStack(self.pot - splitPot)
		
		self.pot = 0
		self.boardCards = []
		for player in self.players:
			player.holeCards = []
			player.bet = 0
		if not self.gui and self.v:
			self.textMoneyState()
		self.updateButton()
		return botWins
		


if __name__ == '__main__':
	gui = False 
	botGameWins = 0
	loseHands = []
	winHands = []
	verbose = True
	numGames = 1
 
	if len(sys.argv) > 1 and sys.argv[1] == "-h":
		botType = -1
	else:
		botType = 2

	for i in range(numGames):
		numHands = 0
		game = PokerGame(gui, 1, botType, verbose)
		while game.players[0].stack > 0 and game.players[1].stack > 0:
			#botHandWins = botWins + game.playHand()	
			game.playHand()
			numHands = numHands + 1
		
		if game.players[0].stack > 0:
			botGameWins = botGameWins + 1
			print "Phil wins the game!"
			winHands.append(numHands)		
		else:
			loseHands.append(numHands)
			print "The Guest has won this time..."
	
		print "[num hands="+str(numHands)+"]"
		
	#print "[numWins="+str(botGameWins)+" out of 100]"
	#print winHands
	#print loseHands 
		

