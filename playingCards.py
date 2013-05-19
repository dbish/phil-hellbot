suits = ['diamond', 'spade', 'heart', 'club']
names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

class Card():
	def __init__(self, suitVal, nameVal):
		self.suitVal = suitVal
		self.nameVal = nameVal

	def suit(self):
		return suits[self.suitVal]

	def name(self):
		return names[self.nameVal]

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
