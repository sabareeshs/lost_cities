from play import Player
def PlayerTest():
	player = Player(5)
	player.add_card((0,6))
	assert(player.play_card((-1, 6), 1) == False) # only 5 colors
	assert(player.play_card((5, 6), 1) == False) # only 5 colors
	assert(player.play_card((0, 6), 1) == True) 
	player.add_card((0,5))
	assert(player.play_card((0, 5), 1) == False) # out of order 
	assert(player.play_card((0, 7), 1) == False) # not in hand
	player.add_card((0,7))
	assert(player.play_card((0, 7), 1) == True)
	assert(player.count() == -7)
	player.add_card((1,1))
	assert(player.play_card((1, 1), 1) == True)
	player.add_card((1,1))
	assert(player.play_card((1, 1), 1) == True)
	player.add_card((1,5))
	assert(player.play_card((1, 5), 1) == True)
	player.add_card((1,5))
	assert(player.play_card((1, 5), 1) == False) # no duplicates other than 1
	player.add_card((1,9))
	assert(player.play_card((1, 9), 1) == True)
	assert(player.play_card((1, 9), 1) == False) # not in hand; already played
	assert(player.count() == 15)
	player.add_card((2,1))
	assert(player.play_card((2, 1), 1) == True)
	player.add_card((2,1))
	assert(player.play_card((2, 1), 1) == True)
	player.add_card((2,1))
	assert(player.play_card((2, 1), 1) == True)
	assert(player.count() == -65)
	player.add_card((2,3))
	assert(player.play_card((2, 3), 0) == True)
	assert(player.count() == -65)
	player.display()
	
PlayerTest()
