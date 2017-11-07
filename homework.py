import sys
from copy import deepcopy

#opening input text
file_input = open('input.txt','r')

#read inputs
board_dimension = int(file_input.readline().rstrip())
game_mode = file_input.readline().rstrip()
XO_player = file_input.readline().rstrip()
depth = int(file_input.readline().rstrip())
dotcount = 0

cell_value = [[0 for x in range(board_dimension)] for y in range(board_dimension)]
for x in range(board_dimension):
	 numbers = file_input.readline().rstrip().split()
	 for y in range(board_dimension):
	 	cell_value[x][y] = int(numbers[y])

board_state = [["" for x in range(board_dimension)] for y in range(board_dimension)]
for x in range(board_dimension):
	line = file_input.readline().rstrip()
	for y in range(board_dimension):
		board_state[x][y] = line[y]
		if line[y] =='.':
			dotcount += 1

def Neighbor(player, row, col, fromwhere):
	tempplayer = "X"
	#need to switch if from MIN and player is X
	if fromwhere == "MIN":
		if player == "X":
			tempplayer = "O"
	else:
		if player == "O":
			tempplayer = "O"

	#check left
	if col != 0:
		if board_state[row][col-1] == tempplayer:
			return True

	#check right
	if col != board_dimension - 1:
		if board_state[row][col+1] == tempplayer:
			return True

	#check bottom
	if row != board_dimension - 1:
		if board_state[row+1][col] == tempplayer:
			return True

	#check top
	if row != 0:
		if board_state[row-1][col] == tempplayer:
			return True

	return False
	

#cutoff function use how many free space is left and how deep we have gone
def Cutoff(blankleft, deepness):
	if blankleft == 0 or deepness <= 0:
		return True
	else:
		return False

def makeMove(player, fromwhere, move, move_x, move_y):
	tempplayer = "X"
	enemyplayer = "O"
	if fromwhere == "MIN":
		if player == "X":
			tempplayer = "O"
			enemyplayer = "X"
	else:
		if player == "O":
			tempplayer = "O"
			enemyplayer = "X"

	#listofenemy = []
	board_state[move_x][move_y] = tempplayer
	if move == "Raid":
		#left
		if move_y != 0:
			if board_state[move_x][move_y-1] == enemyplayer:
				board_state[move_x][move_y-1] = tempplayer
				#listofenemy.append((move_x,move_y-1))
		#right
		if move_y != board_dimension - 1:
			if board_state[move_x][move_y+1] == enemyplayer:
				board_state[move_x][move_y+1] = tempplayer
				#listofenemy.append((move_x,move_y+1))
		#bottome
		if move_x != board_dimension - 1:
			if board_state[move_x+1][move_y] == enemyplayer:
				board_state[move_x+1][move_y] = tempplayer
				#listofenemy.append((move_x+1,move_y))
		#top
		if move_x != 0:
			if board_state[move_x-1][move_y] == enemyplayer:
				board_state[move_x-1][move_y] = tempplayer
				#listofenemy.append((move_x-1,move_y))


def M_MIN(blankleft, deepness):
	#print "MIN"
	#print board_state
	global board_state
	if Cutoff(blankleft, deepness):
		xvalue = 0
		ovalue = 0
		for x in range(board_dimension):
			for y in range(board_dimension):
				if board_state[x][y] == 'X':
					xvalue += cell_value[x][y]
				if board_state[x][y] == 'O':
					ovalue += cell_value[x][y]
		if XO_player == 'X':
			return (xvalue - ovalue)
		else:
			return (ovalue - xvalue)

	value = sys.maxint
	move = []
	raid_space = []
	#loop over stake
	for x in range(board_dimension):
		for y in range(board_dimension):
			if board_state[x][y] == '.':
				if Neighbor(XO_player,x,y,"MIN"):
					raid_space.append((x,y))
				tempboard = deepcopy(board_state)
				makeMove(XO_player, "MIN", "Stake", x, y)
				tempval = M_MAX(blankleft-1,deepness-1)
				#print "mintempval",tempval
				#print "value",value
				if tempval < value:
					value = tempval
					move = (x,y,"Stake")
				board_state = deepcopy(tempboard)
	#loop over raid
	for pair in raid_space:
		tempboard = deepcopy(board_state)
		makeMove(XO_player, "MIN", "Raid", pair[0], pair[1])
		tempval = M_MAX(blankleft-1,deepness-1)
		#print "minraidtempval", tempval
		#print "value", value
		if tempval < value:
			value = tempval
			move = (pair[0],pair[1],"Raid")
		board_state = deepcopy(tempboard)
	if deepness == depth:
		return move
	return value


def M_MAX(blankleft, deepness):
	#print "Max"
	#print board_state
	global board_state
	if Cutoff(blankleft, deepness):
		xvalue = 0
		ovalue = 0
		for x in range(board_dimension):
			for y in range(board_dimension):
				if board_state[x][y] == 'X':
					xvalue += cell_value[x][y]
				if board_state[x][y] == 'O':
					ovalue += cell_value[x][y]
		if XO_player == 'X':
			return (xvalue - ovalue)
		else:
			return (ovalue - xvalue)

	value = -sys.maxint-1
	move = []
	raid_space = []
	#loop over stake
	for x in range(board_dimension):
		for y in range(board_dimension):
			if board_state[x][y] == '.':
				if Neighbor(XO_player,x,y,"MAX"):
					raid_space.append((x,y))
				tempboard = deepcopy(board_state)
				makeMove(XO_player, "MAX", "Stake", x, y)
				tempval = M_MIN(blankleft-1,deepness-1)
				#print "maxtempval",tempval
				#print "value",value
				if tempval > value:
					value = tempval
					move = (x,y,"Stake")
				board_state= deepcopy(tempboard)
	#loop over raid
	for pair in raid_space:
		tempboard = deepcopy(board_state)
		makeMove(XO_player, "MAX", "Raid", pair[0], pair[1])
		tempval = M_MIN(blankleft-1,deepness-1)
		#print "maxraidtempval", tempval
		#print "value", value
		if tempval > value:
			value = tempval
			move = (pair[0],pair[1],"Raid")
		board_state = deepcopy(tempboard)
	if deepness == depth:
		return move
	return value


def AB_MIN(blankleft, deepness, alpha, beta):
	#print "MIN"
	#print board_state
	global board_state
	if Cutoff(blankleft, deepness):
		xvalue = 0
		ovalue = 0
		for x in range(board_dimension):
			for y in range(board_dimension):
				if board_state[x][y] == 'X':
					xvalue += cell_value[x][y]
				if board_state[x][y] == 'O':
					ovalue += cell_value[x][y]
		if XO_player == 'X':
			return (xvalue - ovalue)
		else:
			return (ovalue - xvalue)


	value = sys.maxint
	move = []
	raid_space = []
	#loop over stake
	for x in range(board_dimension):
		for y in range(board_dimension):
			if board_state[x][y] == '.':
				if Neighbor(XO_player,x,y,"MIN"):
					raid_space.append((x,y))
				tempboard = deepcopy(board_state)
				makeMove(XO_player, "MIN", "Stake", x, y)
				value = min(value, AB_MAX(blankleft-1,deepness-1,alpha,beta))
				#print "mintempval",tempval
				#print "value",value
				board_state = deepcopy(tempboard)
				if value < beta:
					beta = value
					move = (x,y,"Stake")
				if beta <= alpha:
					break
	#loop over raid
	for pair in raid_space:
		tempboard = deepcopy(board_state)
		makeMove(XO_player, "MIN", "Raid", pair[0], pair[1])
		value = min(value, AB_MAX(blankleft-1,deepness-1,alpha,beta))
		#print "minraidtempval", tempval
		#print "value", value
		board_state = deepcopy(tempboard)
		if value < beta:
			beta = value
			move = (pair[0],pair[1],"Raid")
		if beta <= alpha:
			break
	if deepness == depth:
		return move
	return value


def AB_MAX(blankleft, deepness, alpha, beta):
	#print "Max"
	#print board_state
	global board_state
	if Cutoff(blankleft, deepness):
		xvalue = 0
		ovalue = 0
		for x in range(board_dimension):
			for y in range(board_dimension):
				if board_state[x][y] == 'X':
					xvalue += cell_value[x][y]
				if board_state[x][y] == 'O':
					ovalue += cell_value[x][y]
		if XO_player == 'X':
			return (xvalue - ovalue)
		else:
			return (ovalue - xvalue)

	value = -sys.maxint-1
	move = []
	raid_space = []
	#loop over stake
	for x in range(board_dimension):
		for y in range(board_dimension):
			if board_state[x][y] == '.':
				if Neighbor(XO_player,x,y,"MAX"):
					raid_space.append((x,y))
				tempboard = deepcopy(board_state)
				makeMove(XO_player, "MAX", "Stake", x, y)
				value = max(value, AB_MIN(blankleft-1,deepness-1,alpha,beta))
				#print "maxtempval",tempval
				#print "value",value
				board_state= deepcopy(tempboard)
				if value > alpha:
					alpha = value
					move = (x,y,"Stake")

				if beta <= alpha:
					break
	#loop over raid
	for pair in raid_space:
		tempboard = deepcopy(board_state)
		makeMove(XO_player, "MAX", "Raid", pair[0], pair[1])
		value = max(value, AB_MIN(blankleft-1,deepness-1,alpha,beta))
		#print "maxraidtempval", tempval
		#print "value", value
		board_state = deepcopy(tempboard)
		if value > alpha:
			alpha = value
			move = (pair[0],pair[1],"Raid")
		if beta <= alpha:
			break
	if deepness == depth:
		return move
	return value




#start algorithm
if game_mode == "MINIMAX":
	move = M_MAX(dotcount, depth)

if game_mode == "ALPHABETA":
	move = AB_MAX(dotcount, depth, (-sys.maxint-1), sys.maxint)


file_input.close()

file_output = open('output.txt','w')
file_output.write(chr(65+move[1])+str(move[0]+1)+" "+move[2]+"\n")
makeMove(XO_player, "MAX", move[2], move[0], move[1])
for state in board_state:
	for x in range(board_dimension):
		file_output.write(state[x])
	file_output.write("\n")

file_output.close()