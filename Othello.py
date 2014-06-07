from copy import deepcopy
from time import time

class TeamA:
     def __init__(self):
          self.size = 4
          self.board = [[' ']*self.size for i in range(self.size)]
          mid = self.size/2
          self.board[mid][mid] = 'W'
          self.board[mid-1][mid] = 'B'
          self.board[mid-1][mid-1] = 'W'
          self.board[mid][mid-1] = 'B'
          self.player_count = self.opp_count = 2
          # a list of unit vectors (row, col)
          self.directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
     
     #Prints the board
     def __repr__(self):
        s = "%s count: %s\n%s count: %s\n\n   " % (self.player, self.player_count, self.opp, self.opp_count)
        s += " ".join([str(i) for i in range(self.size)])
        s += "\n   %s\n" % ('--'*self.size)
        for i in range(self.size):
            s += str(i) + ' |'
            for j in range(self.size):
                s +=  str(self.get_square(i,j)) + '|'
            s += "\n   %s\n" % ('--'*self.size)
        return s
     
     """ ======================== Legal move  ====================== """

     #Checks every direction from the position which is input via "col" and "row", to see if there is an opponent piece
     #in one of the directions. If the input position is adjacent to an opponents piece, this function looks to see if there is a
     #a chain of opponent pieces in that direction, which ends with one of the players pieces. 
     def play_legal_move(self, row, col, player, opp, flip=False):
          # not empty
          if(self.get_square(row,col)!=" "):
               return False
          
          if(player == opp):
               print "player and opponent cannot be the same" 
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

     def evaluate(self): return self.player_count - self.opp_count

     """ ========================= Making moves ==================== """

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
     
     #Search the game board for a legal move, and play the first one it finds
     def make_move(self, player, opp, flip=True):
          for row in range(self.size):
               for col in range(self.size):
                    if self.play_legal_move(row, col, player, opp, flip): return (row,col)
          return (-1,-1)


def minimax(Board, maximizingPlayer, depth, count):
     symbol = {True: 'B', False: 'W'} # maximizing player has 'B' and minimizing 'W'
     player = symbol[maximizingPlayer]
     opp = symbol[not maximizingPlayer]
     moves_list = Board.get_moves_list(player, opp)
     best_move = (-1,-1)
    
     if ( depth==0 or moves_list == [] ):
         best_score = Board.evaluate()
         best_move = (-1, -1)
         return best_score, best_move, count
       
     if maximizingPlayer:
           best_score = float("-inf")
           for move in moves_list:
                new_board = deepcopy(Board)
                new_board.play_legal_move(move[0], move[1], player, opp, flip=True)
                the_score, the_move, count = minimax(new_board, not maximizingPlayer, depth-1, count+1)
                best_score = max(best_score, the_score)
                if (the_score == best_score):
                    best_move = move

           return best_score, best_move, count
     else:
           best_score = float("inf")
           for move in moves_list:
                new_board = deepcopy(Board)
                new_board.play_legal_move(move[0], move[1], player, opp, flip=True)
                the_score, the_move, count = minimax(new_board, not maximizingPlayer, depth-1, count+1)
                best_score = min(best_score, the_score)
                if (the_score == best_score):
                    best_move = move

           return best_score, best_move, count





def makeMove(Board, depth, cpuval, humanval):
    start_time = time() # record time
    bestScore, bestMove, count = minimax(Board, cpuval=='B', depth, 0)
    elapsed_time = time() - start_time
    print "CPU Move: %s, Score: %d" % (bestMove, bestScore)
    Board.play_legal_move(bestMove[0], bestMove[1], cpuval, humanval, flip=True) # play move
    print "Number of nodes searched: %d \nTime taken: %.2f" % (count, elapsed_time)
    return bestMove[0], bestMove[1]


def play():
    Board = TeamA()
    humanval = 'W'
    cpuval = 'B'
    Board.player, Board.opp = cpuval, humanval
    depth = 5 # Number of moves to look ahead
    print Board

    # CPU's initial move if black 
    if cpuval=='B':
     row, col = makeMove(Board, depth, cpuval, humanval) 
     print "%s %s '%s' to (%d, %d) %s" % ('='*10, "CPU moved", cpuval, row, col, '='*10)
     print Board
     print Board.get_moves_list(humanval, cpuval)
     
    while( Board.full_board()==False ):
        # human move
        human_move_possible = Board.any_legal_move(humanval, cpuval)
        # if any human move left
        if human_move_possible: 
             print "\nYour move, pick a row, column e.g. 0,2"
             row, col = input()
             row, col = int(row), int(col)
             if not Board.play_legal_move(row, col, humanval, cpuval): continue
             Board.play_legal_move(row, col, humanval, cpuval, flip=True)
             print "%s %s '%s' to (%d, %d) %s" % ('='*10, "Human moved", humanval, row, col, '='*10)
             print Board
             print Board.get_moves_list(cpuval, humanval)

        # CPU move
        cpu_move_possible = Board.any_legal_move(cpuval, humanval)
        if cpu_move_possible:
             row, col = makeMove(Board, depth, cpuval, humanval) 
             #row, col = Board.make_move(cpuval, humanval)
             print "%s %s '%s' to (%d, %d) %s" % ('='*10, "CPU moved", cpuval, row, col, '='*10)
             print Board
             print Board.get_moves_list(humanval, cpuval)
        # check if no move possible
        if Board.game_end(): break

    print Board
    if(Board.winner()==' '): print "Cat game" 
    elif(Board.winner()==humanval): print "You Win!"
    elif(Board.winner()==cpuval): print "CPU Wins!"

def test():
    Board = TeamA()
    Board.board = [['B','W',' ',' '], \
                   ['B','W','W',' '], \
                   ['B','W','B',' '], \
                   ['W','W','W','B']]                  
    humanval = 'W'
    cpuval = 'B'
    Board.player, Board.opp = cpuval, humanval
    print Board
    print Board.get_moves_list(humanval, cpuval)

    #"""
    row, col = makeMove(Board, 4, cpuval, humanval) 
    print "%s %s '%s' to (%d, %d) %s" % ('='*10, "CPU moved", cpuval, row, col, '='*10)
    print Board
    print Board.get_moves_list(cpuval, humanval)
    
    """
    vals = ['B', 'W']
    moves = [(0,2),(0,3)]
    i=0
    for move in moves:
         player, opp = vals[i%2], vals[(i+1)%2]
         i += 1
         Board.play_legal_move(move[0], move[1], player, opp, flip=True)
         print Board
         print Board.get_moves_list(opp, player)
         if Board.game_end(): print "Winner: %s" % Board.winner()
    """
    
def main(): test()

if __name__ == "__main__": main()
