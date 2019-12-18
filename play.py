from optparse import OptionParser
import time
import random
import os
class Player(object):
	def __init__(self, num_colors):
		assert(num_colors == 5 or num_colors == 6)
		self.colors = ["RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "VIOLET"]
		self.cards = [[] for i in range(num_colors)]
		self.discards = [[] for i in range(num_colors)]
		self.hand = [[] for i in range(num_colors)]
		self.actions = ["DISCARD", "USE"]

	def add_card(self, card):
		color,number = card
		self.hand[color].append(number)

	def check_in_hand(self, color, number):
		return number in self.hand[color]

	# card is a (color,number) tuple
	# hand is 1 and numbers are 2 to 10
	def valid_card(self, color, number):
		if (color < 0 or color >=  len(self.cards)):
			print "***** Invalid color *****"
			return False
		if (number < 1 or number > 10):
			print "***** Invalid number *****"
			return False
		if not self.check_in_hand(color, number):
			print "***** Card not in hand *****"
			return False

	def play_card(self, card, action):
		color,number = card
		if self.valid_card(color, number) == False:
			return False
		if action == 0:
			self.discards[color].append(number)
			self.hand[color].remove(number)
			return True
		if len(self.cards[color]) > 0:
			topnumber = self.cards[color][-1]
			if (topnumber > number):
				print "***** Card not in order *****"
				return False
			if (topnumber == number and number != 1):
				print "***** Card duplicate *****"
				return False
		self.cards[color].append(number)
		self.hand[color].remove(number)
		return True

	def count(self):
		tot = 0;
		for column in self.cards:
			if len(column) > 0:
				multiplier = column.count(1) + 1
				column_total = sum(column)
				if column_total == len(column):
					tot = tot - (20 * multiplier)
				else:
					tot = tot - 20 + (multiplier * (column_total - multiplier + 1))
		return tot

	def display(self):
		for i in range(len(self.cards)):
			print "%8s: %30s %8s %30s" % (self.colors[i], str(self.cards[i]), 'UNUSED :', str(self.discards[i]))

	def show_hand(self):
		print "************************* HAND *******************************"
		for i in range(len(self.hand)):
			print "%8s %30s" % (self.colors[i], str(self.hand[i]))

	def get_card(self, player_num):
		input_color = raw_input('Player ' + str(player_num) + ' Enter color from ' + str(self.colors) + ": ");
		color = self.colors.index(input_color.upper())
		input_number = raw_input('Player ' + str(player_num) + ' Enter number: ')
		number = int(input_number)
		input_action = raw_input('Player ' + str(player_num) + ' Enter action (DISCARD OR USE): ')
		action = self.actions.index(input_action.upper())
		return color, number, action

class AlgoPlayer(Player):
	def __init__(self, num_colors):
		Player.__init__(self, num_colors)

	def get_card(self, player_num):
		while True:
			color = random.randint(0, len(self.hand)-1)
			if len(self.hand[color]) > 0:
				return color, random.choice(self.hand[color]), random.randint(0, len(self.actions)-1)
		
class Board:
	def __init__(self, mode, num_colors):
		assert(mode >=0 and mode <= 2)
		assert(num_colors == 5 or num_colors == 6)
		self.num_colors = num_colors
		self.mode = mode
		if self.mode == 0:
			self.players = [AlgoPlayer(num_colors), Player(num_colors)]
		elif self.mode == 1:
			self.players = [Player(num_colors), Player(num_colors)]
		else:
			self.players = [AlgoPlayer(num_colors), AlgoPlayer(num_colors)]
		random.shuffle(self.players)
		self.colors = ["RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "VIOLET"]
		self.colors = self.colors[0:num_colors]
		self.deck = []
		for color in range(num_colors):
			# add numbers
			for number in range(2,11):
				self.deck.append((color, number))
			# add hands
			for hand in range(3):
				self.deck.append((color, 1))
		random.shuffle(self.deck)

	def display(self, player_num):
		os.system('clear')
		print "************************* BOARD *******************************"
		for i in range(self.num_colors):
			discards = self.players[0].discards[i] + self.players[1].discards[i]
			print "%8s P0: %30s UNUSED: %30s P1: %30s %s" % (self.colors[i], str(self.players[0].cards[i]), str(discards), str(self.players[1].cards[i]), self.colors[i])
		if player_num == 0 or player_num == 1:
			self.players[player_num].show_hand()

	def distribute(self):
		num_cards = 0
		while num_cards < 16:
			player_num = num_cards % 2
			self.players[player_num].add_card(self.deck.pop())
			num_cards = num_cards + 1

	def play(self):
		self.distribute()
		num_cards = 0
		num_turns = (12 * self.num_colors) - 16
		while num_cards < num_turns:
			player_num = num_cards % 2
			while True:
				try:
					if self.mode != 2:
						self.display(player_num)
						print "Remaining cards in deck: ", len(self.deck)
					color, number, action = self.players[player_num].get_card(player_num)
					if (self.players[player_num].play_card((color, number), action)):
						self.players[player_num].add_card(self.deck.pop())
						break
					else:
						if type(self.players[player_num]).__name__ == "Player":
							print "Invalid card(",self.colors[color], ",", number, ",", action, "). Try again"
							dummy = raw_input('Press any button to continue')
				except (ValueError):
					print "Invalid input. Try again"
					dummy = raw_input('Press any button to continue')
			if self.mode == 1:
				os.system('clear')
				print 'Sleeping 3 seconds'
				time.sleep(3)
			num_cards = num_cards + 1
		self.display(-1)
		print "Player 0: ",self.players[0].count()
		print "Player 1: ",self.players[1].count()
			

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-m", "--mode", dest="mode", default=0, type="int",
                  help="0) (default) human vs computer 1) humans 2) computers")
	parser.add_option("-n", "--num_colors", dest="num_colors", type="int", help=" 5(default) or 6", default = 5)

	(options, args) = parser.parse_args()
	board = Board(options.mode, options.num_colors)
	board.play()
