from copy import deepcopy
from time import time

# timeout
import signal
from contextlib import contextmanager

class Gupta_Chou_MacArthur_Almakhdhub:
     def __init__(self):
          self.size = 8
          self.board = [[' ']*self.size for i in range(self.size)]
          mid = int(self.size/2)
          self.board[mid][mid] = 'W'
          self.board[mid-1][mid] = 'B'
          self.board[mid-1][mid-1] = 'W'
          self.board[mid][mid-1] = 'B'
          self.directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

          self.player, self.opp = 'B', 'W'
          self.player_count = self.opp_count = 2
          self.low_depth = 2
          self.depth = 4 # Number of moves to look ahead
          self.time_limit = 15 # choose random move if timed out
          self.debug = False
     
     #Prints the board
     def __repr__(self):
        s = "   " + " ".join([str(i) for i in range(1,self.size+1)])
        s += "\n   %s\n" % ('--'*self.size)
        for i in range(self.size):
            s += str(i+1) + ' |'
            for j in range(self.size):
                s +=  str(self.get_square(i,j)) + '|'
            s += "\n   %s\n" % ('--'*self.size)
        return s

     def print_stats(self, player, row, col):
          if player == self.player: name, player = "CPU moved", self.player
          else: name, player = "Human moved", self.opp
          print("%s %s '%s' to (%d, %d) %s" % ('='*10, name, player, row+1, col+1, '='*10) )
          print("\n%s count: %s\n%s count: %s\n" % (self.player, self.player_count, self.opp, self.opp_count))
          #print( self )
          print("Possible human moves ", self.get_moves_list(self.opp, self.player) )
          print("Possible CPU moves", self.get_moves_list(self.player, self.opp) )
          print("\nNet Score: %.1f \nParity: %.1f, Mobility: %.1f, Stability: %.1f\n" % (self.evaluate()) )
               
     """ ======================== Legal move  ====================== """

     #Checks every direction from the position which is input via "col" and "row", to see if there is an opponent piece
     #in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
     #a chain of opponent pieces in that direction, which ends with one of the players pieces. 
     def play_legal_move(self, row, col, player, opp, flip=False):
          # not empty
          if(self.get_square(row,col)!=" "):
               return False
          
          if(player == opp):
               print("player and opponent cannot be the same")
               return False
          
          legal = False
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
                              legal = True
                              if flip: self.flip_tiles(row, col, Dir, i, player)
                              break
          return legal

     """ ====================== End game functions ================== """

     # Returns true if there is any legal move left for player
     def any_legal_move(self, player, opp):
          for row in range(self.size):
               for col in range(self.size):
                    if self.play_legal_move(row, col, player, opp): return True
          return False
          
     def game_end(self): return ( self.any_legal_move(self.player, self.opp)==False and self.any_legal_move(self.opp, self.player)==False )
     
     def full_board(self):
        for row in range(self.size):
            for col in range(self.size):
                if(self.board[row][col]==' '): return False
        return True

     def winner(self):
          if self.player_count > self.opp_count: return self.player
          elif self.player_count < self.opp_count: return self.opp
          return ' '

     def evaluate(self):
          # check game end
          if self.game_end():
               if self.winner() == self.player: return float("Inf"), -1, -1, -1
               elif self.winner() == self.opp: return float("-Inf"), -1, -1, -1
               else: return 0, -1, -1, -1

          # coin parity
          parity = 100 * ( float(self.player_count - self.opp_count) / (self.player_count + self.opp_count))

          # mobility
          num_player_moves = len(self.get_moves_list(self.player, self.opp))
          num_opp_moves = len(self.get_moves_list(self.opp, self.player))
          mobility = 100 * ( float(num_player_moves - num_opp_moves) / (num_player_moves + num_opp_moves) )

          # corner
          corners = [(0,0), (0, self.size-1), (self.size-1, 0), (self.size-1, self.size-1)]
          player_corners = opp_corners = 0
          for corner in corners:
               if self.get_square(corner[0], corner[1]) == self.player: player_corners += 1
               elif self.get_square(corner[0], corner[1]) == self.opp: opp_corners += 1
               
          if ( player_corners + opp_corners !=0 ):
               stability = 100 * ( float(player_corners - opp_corners) / (player_corners + opp_corners) )
          else: stability = 0
          
          # score
          score = parity/100 + mobility + 10*stability
          return score, parity, mobility, stability
          

     """ ========================= Making moves ==================== """
     
     #returns the value of a square on the board
     def get_square(self, row, col):
          return self.board[row][col]
     
     #sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
     #(dist) to be a given value ( player )
     def flip_tiles(self, row, col, Dir, dist, player):
          for i in range(dist):
               self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
          self.count_pieces(self.player, self.opp)
          return True
     
     # Returns list of legal moves
     def get_moves_list(self, player, opp):
          moves_list = []
          for row in range(self.size):
               for col in range(self.size):
                    if self.play_legal_move(row, col, player, opp): moves_list.append((row, col))
          return moves_list
     
     # Count number of player and opp pieces on the board
     def count_pieces(self, player, opp) :
          player_count = opp_count = 0
          for row in range(self.size):
               for col in range(self.size):
                    if self.get_square(row, col) == player: player_count += 1
                    elif self.get_square(row, col) == opp: opp_count += 1
          self.player_count = player_count
          self.opp_count = opp_count
          return

     def play_square(self, row, col, player, opp):
          self.player, self.opp = player, opp
          # Place a piece of the opponent's color at (row,col)
          if (row,col) != (-1,-1): self.play_legal_move(row,col, opp, player, flip=True)

          # Determine best move and and return value to Matchmaker
          row,  col = make_move(self, player, opp, matchmaker=True)
          if row == -1 and bool(self.get_moves_list(player, opp)):
               row, col = self.get_moves_list(player, opp)[0][0], self.get_moves_list(player, opp)[0][1]
               self.play_legal_move(row, col, player, opp, flip=True)
          return row, col
          
          


""" ========================= minimax and other functions ==================== """

class TimeoutException(Exception): pass
def timeout(fun, limit, *args ):
   @contextmanager
   def time_limit(seconds):
       def signal_handler(signum, frame):
           raise TimeoutException
       signal.signal(signal.SIGALRM, signal_handler)
       signal.alarm(seconds)
       try:
           yield
       finally:
           signal.alarm(0)
   try:
       with time_limit(limit):
           return fun(*args)
   except TimeoutException:
       return [None]*3

def minimax(Board, maximizingPlayer, depth, count):
     # maximizing player has 'B' and minimizing 'W'
     if maximizingPlayer: player, opp = Board.player, Board.opp
     else: player, opp = Board.opp, Board.player
     
     moves_list = Board.get_moves_list(player, opp)
     best_move = (-1,-1)

     # base case
     if ( depth==0 or moves_list == [] ):
         best_score, parity, mobility, stability = Board.evaluate()
         best_move = (-1, -1)
         return best_score, best_move, count

     # maximizing player
     if maximizingPlayer:
           best_score = float("-inf")
           for move in moves_list:
                new_board = deepcopy(Board)
                new_board.play_legal_move(move[0], move[1], player, opp, flip=True)
                the_score, the_move, count = minimax(new_board, False, depth-1, count+1)
                best_score = max(best_score, the_score)
                if (the_score == best_score):
                    best_move = move

           return best_score, best_move, count
     # minimzing player
     else:
           best_score = float("inf")
           for move in moves_list:
                new_board = deepcopy(Board)
                new_board.play_legal_move(move[0], move[1], player, opp, flip=True)
                the_score, the_move, count = minimax(new_board, True, depth-1, count+1)
                best_score = min(best_score, the_score)
                if (the_score == best_score):
                    best_move = move

           return best_score, best_move, count

         
def alphabeta(Board, maximizingPlayer, depth, count, alpha, beta):
     # maximizing player has 'B' and minimizing 'W'
     if maximizingPlayer: player, opp = Board.player, Board.opp
     else: player, opp = Board.opp, Board.player
     
     moves_list = Board.get_moves_list(player, opp)
     best_move = (-1,-1)

     # base case
     if ( depth==0 or moves_list == [] ):
         best_score, parity, mobility, stability = Board.evaluate()
         best_move = (-1, -1)
         return best_score, best_move, count

     # maximizing player
     if maximizingPlayer:
           best_score = float("-inf")
           for move in moves_list:
                new_board = deepcopy(Board)
                new_board.play_legal_move(move[0], move[1], player, opp, flip=True)
                the_score, the_move, count = alphabeta(new_board, False, depth-1, count+1, alpha, beta)
                if (the_score > alpha):
                    alpha = the_score
                    best_move = move
                if beta <= alpha: break

           return alpha, best_move, count
     # minimzing player
     else:
           best_score = float("inf")
           for move in moves_list:
                new_board = deepcopy(Board)
                new_board.play_legal_move(move[0], move[1], player, opp, flip=True)
                the_score, the_move, count = alphabeta(new_board, True, depth-1, count+1, alpha, beta)
                if (the_score < beta):
                    beta = the_score
                    best_move = move
                if beta <= alpha: break

           return beta, best_move, count



def make_move(Board, player, opp, matchmaker=False):
     # prune
     prune = True
     
     # check if any possible
     move_possible = Board.any_legal_move(player, opp)
     if not move_possible:
          print("No possible move!")
          return (-1, -1)
     
     # get move
     if matchmaker: row, col, count, elapsed_time = cpu_move(Board, prune)
     elif player==Board.player: row, col, count, elapsed_time = cpu_move(Board, prune)
     else: row, col = human_move(Board)

     # play if legal, else try again
     if not Board.play_legal_move(row, col, player, opp, flip=True): return (-1, -1)

     # print
     if Board.debug:
          print()
          Board.print_stats(player, row, col)
          if player==Board.player: print("Number of nodes searched: %d \nTime taken: %.2f\n" % (count, elapsed_time))
          print("%s" % ('='*40))
     return row, col

def cpu_move(Board, prune):
     # adjust depth according to game state
     num_pieces = Board.player_count + Board.opp_count
     if (num_pieces <= 8 or num_pieces >= 45): depth = Board.depth + 1
     else: depth = Board.depth
     #print("%s Player C using depth: %d %s" % ('='*10, depth, '='*10) )

     # get a quick low depth move
     start_time = time()
     if prune: low_score, low_move, count = alphabeta(Board, True, Board.low_depth, 0, float("-Inf"), float("Inf"))
     else: low_score, low_move, count = minimax(Board, True, Board.low_depth, 0)
     elapsed_time = time() - start_time + 0.1

     # use remining time for a deeper search
     start_time = time()
     if prune: best_score, best_move, count = timeout(alphabeta, int(Board.time_limit - elapsed_time), Board, True, depth, 0, float("-Inf"), float("Inf"))
     else: best_score, best_move, count = timeout(minimax, int(Board.time_limit - elapsed_time), Board, True, depth, 0)
     

     # if timed out, use low depth move
     if best_move==None:
          #print("%s Using low depth move %s" % ('='*10, '='*10) )
          best_score, best_move = low_score, low_move
     
     elapsed_time = time() - start_time
     return best_move[0], best_move[1], count, elapsed_time


def human_move(Board):
     print("\nYour move, pick a row, column e.g. 0,2")
     move = input().split(',')
     row, col = int(move[0])-1, int(move[1])-1
     return row, col


def play():
    Board = Gupta_Chou_MacArthur_Almakhdhub()
    print(Board)

    # CPU's initial move if black 
    if Board.player=='B': make_move(Board, Board.player, Board.opp)
     
    while( Board.game_end()==False ):
        # human move
        make_move(Board, Board.opp, Board.player)
        
        # cpu move 
        if not Board.game_end(): make_move(Board, Board.player, Board.opp)

    if(Board.winner()==' '): print("Cat game") 
    elif(Board.winner()==Board.opp): print("You Win!")
    elif(Board.winner()==Board.player): print("CPU Wins!")


#def main(): play()

#if __name__ == "__main__": main()
