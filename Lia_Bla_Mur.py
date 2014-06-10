import heapq
import time
import random

class Lia_Bla_Mur:

	def __init__(self):
		self.board = [[' ']*8 for i in range(8)]
		self.size = 8
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		# a list of unit vectors (row, col)
		self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]
		self.bestMove = (-1, -1)

#prints the boards
	def PrintBoard(self):
		# Print column numbers
		print("  ",end="")
		for i in range(self.size):
			print(i+1,end=" ")
		print()

		# Build horizontal separator
		linestr = " " + ("+-" * self.size) + "+"

		# Print board
		for i in range(self.size):
			print(linestr)					   # Separator
			print(i+1,end="|")				   # Row number
			for j in range(self.size):
				print(self.board[i][j],end="|")  # board[i][j] and pipe separator 
			print()							  # End line
		print(linestr)

# CHECKS IF A PARTICULAR SQUARE IS LEGAL
#checks every direction fromt the position which is input via "col" and "row", to see if there is an opponent piece
#in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
#a chain of opponent pieces in that direction, which ends with one of the players pieces.	
	def islegal(self, row, col, player, opp):
		if(self.get_square(row,col)!=" "):
			return False
		for Dir in self.directions:
			for i in range(self.size):
				if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
					#does the adjacent square in direction dir belong to the opponent?
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
						#no pieces will be flipped in this direction, so skip it
						break
					#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
					#of opponent pieces
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
						break

					#with one of player's pieces at the other end
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
						#set a flag so we know that the move was legal
						return True
		return False

		
#returns true if the square was played, false if the move is not allowed
	def place_piece(self, row, col, player, opp):
		if(self.get_square(row,col)!=" "):
			return False
		
		if(player == opp):
			print("player and opponent cannot be the same")
			return False
		
		legal = False
		#for each direction, check to see if the move is legal by seeing if the adjacent square
		#in that direction is occuipied by the opponent. If it isnt check the next direction.
		#if it is, check to see if one of the players pieces is on the board beyond the oppponents piece,
		#if the chain of opponents pieces is flanked on both ends by the players pieces, flip
		#the opponents pieces 
		for Dir in self.directions:
			#look across the length of the board to see if the neighboring squares are empty,
			#held by the player, or held by the opponent
			for i in range(self.size):
				if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
					#does the adjacent square in direction dir belong to the opponent?
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= opp and i==1 : # no
						#no pieces will be flipped in this direction, so skip it
						break
					#yes the adjacent piece belonged to the opponent, now lets see if there are a chain
					#of opponent pieces
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
						break

					#with one of player's pieces at the other end
					if self.get_square(row+ i*Dir[0], col + i*Dir[1])==player and i!=0 and i!=1 :
						#set a flag so we know that the move was legal
						legal = True
						self.flip_tiles(row, col, Dir, i, player)
						break

		return legal

	def undo_play(self,boardCopy):
		for i in range(self.size):
			for j in range(self.size):
				self.board[i][j] = boardCopy[i][j]

	def makeACopy(self):
		boardCopy = [[' ']*8 for i in range(8)]
		for i in range(self.size):
			for j in range(self.size):
				boardCopy[i][j] = self.board[i][j]
		return boardCopy		

	def numberOfLegalMoves(self,player,other):
		countPlayer = 0
		countOther = 0
		for i in range(self.size):
			for j in range(self.size):
				if self.islegal(player,other):
					countPlayer += 1
				if self.islegal(other,player):
					countOther += 1
		return countPlayer,countOther

#Places piece of opponent's color at (row,col) and then returns 
#  the best move, determined by the make_move(...) function
	def play_square(self, row, col, playerColor, oppColor):		
		# Place a piece of the opponent's color at (row,col)
		if (row,col) != (-1,-1):
			self.place_piece(row,col,oppColor,playerColor)
		
		# Determine best move and and return value to Matchmaker
		return self.make_move(playerColor, oppColor)

#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
	def flip_tiles(self, row, col, Dir, dist, player):
		for i in range(dist):
			self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
		return True
	
#returns the value of a square on the board
	def get_square(self, row, col):
		return self.board[row][col]

#Search the game board for a legal move, and play the first one it finds
	def make_move(self, playerColor, oppColor):
		ans = MinMax(self, playerColor, oppColor, depth=5)
		return ans

# Evaluate: each disc is worth 0.01; a legal move is worth 1; a corner spot is worth 10.
	def eval_function(self, player, opp):
		score = 0.0
		for row in range (self.size):
			for col in range(self.size):
				if self.get_square(row, col) == opp:
					score -= 0.01
				if self.get_square(row, col) == player:
					score += 0.01
				if self.islegal(row, col, player, opp):
					score += 4
				if (row == 0 and col == 0) or (row == 0 and col == self.size) or (row == self.size and col == 0) or (row == self.size and col == self.size):
					if self.get_square(row, col) == opp:
						score -= 10
					elif self.get_square(row, col) == player:
						score += 10
				if (row == 1 and col == 1) or (row == 1 and col == 6) or (row == 6 and col == 1) or (row == 6 and col == 6):
					if self.get_square(row, col) == opp:
						score += 2
					elif self.get_square(row, col) == player:
						score -= 2
		return score
    
	def gameOver(self):
		countW = 0
		countB = 0
		for i in range(self.size):
			for j in range(self.size):
				if self.board[i][j] == 'W':
					countW += 1
				elif self.board[i][j] == 'B':
					countB += 1
				else :
					return None
		return 'W' if countW>countB else 'B'

def iterativeDeepining(game, player, other, startTime, depth=1, toggle=0, currentDepth=0, maxint=100000):
	if time.time()-startTime >= 14.5: return (game.eval_function(player,other),None)

	test = game.gameOver()

	if test == player:
		return (maxint,None)

	elif test == other:
		return (-maxint,None)

	else:
		if currentDepth<depth :
			if toggle == 0 :
				best_move = (-maxint,None)
				for i in random.sample(range(game.size),game.size):
					for j in random.sample(range(game.size),game.size):
						if game.islegal(i, j, player, other):

							boardCopy = game.makeACopy()
							game.place_piece(i,j,player,other)
							move = iterativeDeepining(game, player, other, startTime, depth, toggle=1, currentDepth=currentDepth+1)
							game.undo_play(boardCopy)

							if move[0] >= best_move[0] :
								best_move = (move[0],i,j)
				return best_move

			else:
				best_move = (maxint,None)
				for i in random.sample(range(game.size),game.size):
					for j in random.sample(range(game.size),game.size):
						if game.islegal(i, j, other, player):
							
							boardCopy = game.makeACopy()
							game.place_piece(i,j,other,player)
							move = iterativeDeepining(game, player, other, startTime, depth, toggle=0, currentDepth=currentDepth)
							game.undo_play(boardCopy)

							if move[0] <= best_move[0]:
								best_move = (move[0],i,j)
				return best_move
		else:
			return (game.eval_function(player,other),None)

def MinMax(board, player, other, depth):
        startTime = time.time()
        move = iterativeDeepining(board,player,other, startTime, depth)
        return move[1],move[2]

if __name__ == "__main__":
	game = Lia_Bla_Mur()
	player = 'W'
	opp = 'B'
	while not game.gameOver():
		game.PrintBoard()
		player1 = (4,4)
		while not game.islegal(player1[0], player1[1], player, opp):
			startTime = time.time()
			player1 = MinMax(game, player, opp, startTime, depth=5)
			print("Time take by player 1 : ", time.time()-startTime)

		print("Player 1 move : ",(player1[0]+1,player1[1]+1))
		game.place_piece(player1[0], player1[1], player, opp)
		print ("Player 1 eval:",game.eval_function(player,opp))

		game.PrintBoard()
		player2 = (4,4)
		while not game.islegal(player2[0], player2[1], opp, player):
			startTime = time.time()
			player2 = MinMax(game, opp, player, startTime, depth=5)
			print("Time take by player 2 : ", time.time()-startTime)
		
		print("Player 2 move : ",(player2[0]+1,player2[1]+1))
		game.place_piece(player2[0], player2[1], opp, player)
		print ("Player 2 eval:",game.eval_function(opp, player))
		
		print("-------------------------------------------------------------------")
	print ("Game won by:",game.gameOver())
