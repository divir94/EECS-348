
import copy
import time

class ShikharA:

	def __init__(self):
		self.board = [[' ']*8 for i in range(8)]
		self.now = time.time()
		self.size = 8
		self.board[4][4] = 'W'
		self.board[3][4] = 'B'
		self.board[3][3] = 'W'
		self.board[4][3] = 'B'
		# a list of unit vectors (row, col)
		self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1)]

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

#Places piece of opponent's color at (row,col) and then returns 
#  the best move, determined by the make_move(...) function
	def play_square(self, row, col, playerColor, oppColor):		
		# Place a piece of the opponent's color at (row,col)
		if (row,col) != (-1,-1):
			self.place_piece(row,col,oppColor,playerColor)
		
		# Determine best move and and return value to Matchmaker
		[cr, cc] = self.make_move(playerColor, oppColor)
		if(cr == -1):
                        posMoves = self.possibleMoves(playerColor, oppColor)
                        #print("playing default %i , %i" %(posMoves[0][0],posMoves[0][1]))
                        cr = posMoves[0][0]
                        cc = posMoves[0][1]
		self.place_piece(cr,cc,playerColor, oppColor)
		#print("playing %i , %i" %(cr+1,cc+1))
		return [cr, cc]

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
		posMoves = self.possibleMoves(playerColor, oppColor)
		print("Printing possible moves")
		for move in posMoves:
			move[0] = move[0]+1
			move[1] = move[1]+1
			print(move)

		depth = 2
		self.now = time.time()
		boardCopy = copy.deepcopy(self)
		[bestmove, bestscore] = self.max_ab(boardCopy, -1000, 1000, playerColor, oppColor,depth)
		return bestmove



	def max_ab(self, b, alpha, beta, playerColor, oppColor, depth):
		bestscore = -10000
		bestmove = [-1,-1]

		moves = b.possibleMoves(playerColor,oppColor)

		for position in moves:
			boardCopy = copy.deepcopy(b)
			boardCopy.place_piece(position[0],position[1],playerColor, oppColor)
			if(boardCopy.board_full()==True or depth == 0 or (time.time()-self.now > 14)):
				thisScore = boardCopy.score(playerColor, oppColor)

			else:
				movPos, thisScore = self.min_ab(boardCopy,alpha, beta, oppColor, playerColor, depth-1)

			if(thisScore > bestscore):
		        #print "updating max score"
				bestscore = thisScore
				bestmove = position

			if (bestscore >= beta):
				return bestmove, bestscore

			alpha = max(alpha,bestscore)

		return bestmove, bestscore

	def min_ab(self, b, alpha, beta, playerColor, oppColor, depth):
		bestscore = 10000
		bestmove = [-1,-1]

		moves = b.possibleMoves(playerColor,oppColor)

		for position in moves:
			boardCopy = copy.deepcopy(b)
			boardCopy.place_piece(position[0],position[1],playerColor, oppColor)
			if(boardCopy.board_full()==True or depth == 0 or (time.time()-self.now > 14)):
				thisScore = boardCopy.score(oppColor, playerColor)

			else:
				movPos, thisScore = self.max_ab(boardCopy,alpha, beta, oppColor, playerColor, depth-1)

			if(thisScore < bestscore):
		        #print "updating max score"
				bestscore = thisScore
				bestmove = position

			if (bestscore <= alpha):
				return bestmove, bestscore

			beta = min(beta,bestscore)

		return bestmove, bestscore
           
   


	def board_full(self):
		for i in range(self.size):
			for j in range(self.size):
				if self.get_square(i,j)==" ":
					return False
		return True

	def current_winner(self):
		numW = 0
		numB = 0
		for i in range(self.size):
			for j in range(self.size):
				if self.get_square(i,j)=="B":
					numB = numB +1
				elif(self.get_square(i,j)=="W"):
					numW = numW +1

		if(numW>numB):
			return 'W'
		elif(numW<numB):
			return 'B'
		else:
			return -1

	def current_winner_score(self):
		numW = 0
		numB = 0
		for i in range(self.size):
			for j in range(self.size):
				if self.get_square(i,j)=="B":
					numB = numB +1
				elif(self.get_square(i,j)=="W"):
					numW = numW +1

		if(numW>numB):
			return numW
		elif(numW<numB):
			return numB
		else:
			return -1

	def isGameOver(self):
		if(self.board_full() or (not self.has_move('B','W') and not self.has_move('B','W'))):
			print("Game is over")
			return True
		return False


####################Player functions#########################
	def possibleMoves(self, player, opp):
		possibleMoves = []
		for i in range(self.size):
			for j in range(self.size):
				if(self.islegal(i,j,player, opp)):
                    # appends row(i) and col(j) to output possibleVals array
					possibleMoves.append([i,j])
		return possibleMoves

	def has_move(self, player, opp):
		for i in range(self.size):
			for j in range(self.size):
				if self.islegal(i,j,player,opp):
					return True
		return False

	####################Evaluation functions#####################

	def score(self, playerColor, oppColor):
		if(self.isGameOver() and self.current_winner() == playerColor):
			return 1000
		if(self.isGameOver() and not self.current_winner() == playerColor):
			return -1000
		# normalize based on the maximum value
		disc_count = self.count_discs(playerColor)/64
		opp_mov = self.num_opponent_moves(playerColor, oppColor)/32
		pos_val = self.position_val(playerColor, oppColor)/620
		#print("disc_count: " + str(disc_count))
		#print("opp_mov: " + str(opp_mov))
		#print("pos_val:" + str(pos_val))
		return disc_count/100 - 1*opp_mov + 10*pos_val

	def count_discs(self, playerColor):
		disc_count = 0;
		for i in range(self.size):
			for j in range(self.size):
				if self.get_square(i,j)==playerColor:
					disc_count = disc_count +1
		return disc_count

	def num_opponent_moves(self, playerColor, oppColor):
		return len(self.possibleMoves(oppColor, playerColor))

	def position_val(self, playerColor, oppColor):
		val = 0
		for i in range(self.size):
			for j in range(self.size):
				piece = 1
				if i == 0 or i == self.size:
					piece += 5
				if j == 0 or j == self.size:
					piece += 5
				# penalty for putting a piece close to the edge
				if i == 1 or i == (self.size -1):
					piece -= 5
				if j == 1 or j == (self.size -1):
					piece -=5

				if self.board[i][j] == playerColor:
					val += piece
				elif self.board[i][j] == oppColor:
					val -= piece

		return val


def main():
	b = TeamA()
	b.PrintBoard()

	humanFirst = input("Will human go first? (Y/N)")
	if humanFirst.lower() == 'y':
		Human = 'B'
		CPU = 'W'
		First = Human
		print("Human is first, color is black")
	else:
		Human = 'W'
		CPU = 'B'
		First = CPU
		print("Human is second, color is white")


	while(not b.isGameOver()):
    	
		HumanMove =[-1,-1];

		if First==Human:
			posMoves = b.possibleMoves(Human, CPU)
			print("Printing possible moves")
			for move in posMoves:
				move[0] = move[0]+1
				move[1] = move[1]+1
				print(move)

			while(True and b.has_move(Human,CPU)):
				row = int(input("Pick a row (1-8): "))
				col = int(input("Pick a col (1-8): "))

				if(row > 0 and row <= b.size and col > 0 and col <= b.size and b.islegal(row-1,col-1, Human, CPU)):
					print("Making move")
					HumanMove =[row-1,col-1];
					break
				
				print("Illegal move.")

		now = time.time()
		CPUMove = b.play_square(HumanMove[0],HumanMove[1], CPU, Human)
		moveTime = time.time() - now
		print (moveTime)
		b.PrintBoard()
		if b.isGameOver():
			break
		print("CPU has played row: %i col: %i" % (CPUMove[0]+1, CPUMove[1]+1))
		b.place_piece(CPUMove[0], CPUMove[1],CPU, Human)
		print( "current winner is " + b.current_winner() + " with a score of %i" % b.current_winner_score())
		b.PrintBoard()
		if b.isGameOver():
			break
		First = Human

	print("Game over")
	print( "winner is " + b.current_winner() + " with a score of %i" % b.current_winner_score())

def main2():
   Human = 'B'
   CPU='W'
   print('Human: B\nCPU:: W\nHuman plays first.')
   player = Human
   opp = CPU

   b = TeamA()
   b.PrintBoard()
   c = TeamA()

   print("B starting the game and playing as " + CPU)
   [i,j] = [-1,-1]
   while(b.board_full()==False):
       k,l = c.play_square(i,j, Human, CPU)
       c.PrintBoard()

       i,j= b.play_square(k,l, CPU, Human)
       b.PrintBoard()
      
   print( "winner is " + b.current_winner() + " with a score of %i" % b.current_winner_score())




