import time
import copy
import random

class DoubleA:

    def __init__(self):
        # Board Initialization
        self.board = [[' ']*8 for i in range(8)]
        self.size = 8
        self.board[4][4] = 'W'
        self.board[3][4] = 'B'
        self.board[3][3] = 'W'
        self.board[4][3] = 'B'
        self.filled_tiles = 4

        # A stack of saved states (for recursive searching of boards)
        self.saved_states = []
        
        # Constants
        self.directions = [ (-1,-1), (-1,0), (-1,1), (0,-1),(0,1),(1,-1),(1,0),(1,1) ]
        self.WINSCORE = 1000000
        self.LOSESCORE = -1000000
        self.MAXTIME = 14.9

        # Weights Initialization
        self.weights = [
                [120, -40,  -5, -15, -15,  -5, -40, 120],
                [-40, -60, -10, -10, -10, -10, -60, -40],
                [ -5, -10, -10,  -3,  -3, -10, -10,  -5],
                [-15, -10,  -3,  -1,  -1,  -3, -10, -15],
                [-15, -10,  -3,  -1,  -1,  -3, -10, -15],
                [ -5, -10, -10,  -3,  -3, -10, -10,  -5],
                [-40, -60, -10, -10, -10, -10, -60, -40],
                [120, -40,  -5, -15, -15,  -5, -40, 120]]

#########################################################
# BOILERPLATE
#########################################################
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
            print(linestr)                     # Separator
            print(i+1,end="|")                 # Row number
            for j in range(self.size):
                print(self.board[i][j], end="|")  # board[i][j] and pipe separator
            print()                           # End line
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
        self.start = time.time()

        if (row,col) != (-1,-1):
            self.filled_tiles += 1
            self.place_piece(row,col,oppColor,playerColor)
            
        # Determine best move and and return value to Matchmaker
        best_move = self.make_move(playerColor, oppColor)
        
        if best_move != (-1,-1):
            self.filled_tiles += 1

        return best_move

#sets all tiles along a given direction (Dir) from a given starting point (col and row) for a given distance
# (dist) to be a given value ( player )
    def flip_tiles(self, row, col, Dir, dist, player):
        for i in range(dist):
            self.board[row+ i*Dir[0]][col + i*Dir[1]] = player
        return True
    
#returns the value of a square on the board
    def get_square(self, row, col):
        return self.board[row][col]

    def propagate_move(self, row, col, playerColor, oppColor):
        '''
        Plays a move and propagates its consequences
        '''
        if (row,col) == (-1,-1): return
        assert row >= 0 and col >=0            
        for Dir in self.directions:
            #look across the length of the board to see if the neighboring squares are empty,
            #held by the player, or held by the opponent
            for i in range(self.size):
                if  ((( row + i*Dir[0])<self.size)  and (( row + i*Dir[0])>=0 ) and (( col + i*Dir[1])>=0 ) and (( col + i*Dir[1])<self.size )):
                    #does the adjacent square in direction dir belong to the opponent?
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])!= oppColor and i==1 : # no
                        #no pieces will be flipped in this direction, so skip it
                        break
                    #yes the adjacent piece belonged to the opponent, now lets see if there are a chain
                    #of opponent pieces
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==" " and i!=0 :
                        break

                    #with one of player's pieces at the other end
                    if self.get_square(row+ i*Dir[0], col + i*Dir[1])==playerColor and i!=0 and i!=1 :
                        #set a flag so we know that the move was legal
                        legal = True
                        self.flip_tiles(row, col, Dir, i, playerColor)
                        break

    def save_state(self):
        state_vars = ['board']
        state = {'board' : self.copy_board()}
        self.saved_states.append(state)

    def copy_board(self):
        new_board = [[a for a in row] for row in self.board]
        return new_board

    def load_state(self):
        state = self.saved_states.pop()
        for var,val in state.items():
            setattr(self, var, val)

    def make_move(self, playerColor, oppColor):
        row,col = self.choose_move(playerColor, oppColor)
        self.propagate_move(row, col, playerColor, oppColor)
        return row,col
            
#########################################################
# DECISION-MAKING RECURSION
#########################################################


    def enumerate_moves(self, playerColor, oppColor):
        '''
        Enumerates all possible moves given a game board
        '''
        possible_moves = [(i,j) 
                          for i in range(self.size) 
                          for j in range(self.size) 
                          if self.islegal(i,j,playerColor,oppColor)]
        random.shuffle(possible_moves)
        return possible_moves

    def alphabeta(self, playerColor, oppColor, reward_fn):
        '''
        Searches moves via alphabeta search with iterative deepening, evaluating outcomes using <reward_fn>
        '''
        
        STARTDEPTH = 2
        MAXDEPTH = 5

        move_scores = {(-1,-1) : -float('Inf')}
        best_val = -float('Inf')
        best_move = (-1,-1)
        
        possible_moves = self.enumerate_moves(playerColor, oppColor)
        if len(possible_moves) == 1: return possible_moves[0]

        for move in possible_moves:
            move_scores[move] = 0
            
        # ----- BEGIN SEARCH -----
        unfilled_tiles = self.size*self.size - self.filled_tiles
        for depth in range(min(STARTDEPTH, unfilled_tiles), MAXDEPTH):

            # If the best value found so far is a win, then return
            if compare_score(best_val,self.WINSCORE) == 0:
                break
            
            # Initalize alpha and beta to the worst case            
            alpha = self.LOSESCORE
            beta = self.WINSCORE
            
            # For every possible move...
            for row,col in possible_moves:

                if best_val == self.WINSCORE:
                    break

                known_score = move_scores[(row,col)]
                # If this branch has already been explored to a game outcome, ignore it
                if not (compare_score(known_score,self.WINSCORE) == 0 or compare_score(known_score,self.LOSESCORE) == 0):
                    
                    # ** State mutated here **
                    self.save_state()
                    self.propagate_move(row,col,playerColor,oppColor)
                    max_min_val = self.min_outcome(alpha, beta, playerColor, oppColor, depth, True, reward_fn)
                    self.load_state()
                    # ** State restored here **

                    if max_min_val is None:
                        # This only occurs if we run out of time; in this case, return the best solution found so far.
                        break

                    alpha = get_max(max_min_val, alpha)

                    # Reset board
                    move_scores[(row,col)] = max_min_val

                    # Update the best value so far if necessary
                    score_diff = compare_score(max_min_val,best_val)
                    if score_diff >= 0:
                        if score_diff == 0:
                            new_weight = self.weights[row][col]
                            old_weight = self.weights[best_move[0]][best_move[1]]

                            if new_weight > old_weight:
                                best_move = (row,col)
                                best_val = max_min_val
                        else:
                            best_move = (row,col)
                            best_val = max_min_val



        return best_move

    def get_outcome(self,eval_fn, alpha, beta, playerColor, oppColor, depth, prev_player_moved, reward_fn):
        '''
        Base function for the max/min steps used in maximin and alpha-beta search
        '''
        if time.time() - self.start >= self.MAXTIME:
            return None
        # If eval_fn is max, return the max outcome; if eval_fn is min, return the min outcome.
        # board.checks += 1
        # All values that are different between max and min are assigned here:

        if eval_fn is get_max:
            new_fn = lambda new_alpha,curr_player_moved: self.min_outcome(new_alpha, beta, playerColor, oppColor, depth, curr_player_moved, reward_fn)
            val_to_assign = playerColor # self.value
            opp_val_to_assign = oppColor
            best_val = alpha
            best_possible_value = self.WINSCORE
            
        elif eval_fn is get_min:
            new_fn = lambda new_beta,curr_player_moved: self.max_outcome(alpha, new_beta, playerColor, oppColor, depth-1, curr_player_moved, reward_fn)
            val_to_assign = oppColor # self.opponent_value()
            opp_val_to_assign = playerColor
            best_val = beta
            best_possible_value = self.LOSESCORE
            
        possible_moves = self.enumerate_moves(val_to_assign, opp_val_to_assign)
        # Recursive stopping condition: if the board is full or a player has already won, return the outcome
        if compare_score(best_val, best_possible_value) == 0:
            return best_val
        
        if depth == 0:
            return reward_fn(False, playerColor, oppColor)

        # If there are no possible moves...
        if not possible_moves:
            if not prev_player_moved: # If the previous player didn't move, then the game is over
                return reward_fn(True, playerColor, oppColor)
            else:
                return new_fn(best_val, False) # If the previous player did move, make no move and tell the next player that you didn't move

        # For every possible move...
        for row,col in possible_moves:
            # ** State mutated here **
            self.save_state()
            self.propagate_move(row,col,val_to_assign, opp_val_to_assign)
            outcome = new_fn(best_val, True)
            self.load_state()
            # ** State restored here **
            if outcome is None: # Only occurs if you run out of time
                return None
            best_val = eval_fn(outcome, best_val)
        return best_val

    def max_outcome(self, alpha, beta, playerColor, oppColor, depth, prev_player_moved, reward_fn):
        return self.get_outcome(get_max, alpha, beta, playerColor, oppColor, depth, prev_player_moved, reward_fn)

    def min_outcome(self, alpha, beta, playerColor, oppColor, depth, prev_player_moved, reward_fn):
        return self.get_outcome(get_min, alpha, beta, playerColor, oppColor, depth, prev_player_moved, reward_fn)

####################################
# LOGIC
####################################

    def choose_move(self, playerColor, oppColor):
        if self.filled_tiles <= 50:
            move = self.alphabeta(playerColor, oppColor, self.stablecount_mincount)
        else:
            move = self.alphabeta(playerColor, oppColor, self.count_tiles)
        return move

    def count_tiles(self, game_over, playerColor, oppColor):
        '''
        Evaluation function that takes the difference between DoubleA's number of tiles under control and its opponent's
        '''
        player_tiles = sum([self.get_square(i,j) == playerColor
                            for i in range(self.size)
                            for j in range(self.size)])
        opp_tiles = sum([self.get_square(i,j) == oppColor
                         for i in range(self.size)
                         for j in range(self.size) ])

        result = player_tiles - opp_tiles

        if game_over:
            if result < 0:
                return self.LOSESCORE
            elif result > 0:
                return self.WINSCORE
            else:
                return 0
        else:
            return result

    def minimize_tiles(self, game_over, playerColor, oppColor):
        '''
        The opposite of count_tiles
        '''
        if game_over:
            return self.count_tiles(True, playerColor, oppColor)
        else:
            return -self.count_tiles(False, playerColor, oppColor)
            
    
    def count_stable_tiles(self, game_over, playerColor, oppColor):
        '''
        Counts the number of stable tiles owned by DoubleA and subtracts the number owned by its opponents. Corners are weighted much more heavily.
        '''
        if game_over:
            return self.count_tiles(True, playerColor, oppColor)
        
        stable_board = [[0]*self.size for i in range(8)]
        def is_stable(row, col,sign):
            if not on_board(row,col):
                return True
            else:
                val = stable_board[row][col]
                return (False if val is 0 else val/abs(val) == sign)
        def on_board(row,col):
            return not(row >= self.size or col >= self.size or row < 0 or col < 0)

        def get_diagonals(row,col):
            return [[(row + i, row +j)
                    for i,j in zip(range(self.size), range(self.size))
                    if on_board(row + i, row + j)] 
                    + [(row - i, row - j)
                    for i,j in zip(range(self.size), range(self.size))
                    if on_board(row + i, row + j)],
                    [(row + i, row - j)
                    for i,j in zip(range(self.size), range(self.size))
                    if on_board(row + i, row +j)] 
                    + [(row - i, row + j)
                    for i,j in zip(range(self.size), range(self.size))
                    if on_board(row + i,row + j)]]

        corners = [(0,0), (0,self.size-1), (self.size-1, 0), (self.size - 1, self.size - 1)]
        checked = set(corners)
        queue = []
        
        # Check for filled columns and rows
        filled_columns = [k for k in range(self.size)
                          if len([l for l in range(self.size) if self.get_square(l,k) != ' ']) == self.size]
        filled_rows = [k for k in range(self.size)
                          if len([l for l in range(self.size) if self.get_square(k,l) != ' ']) == self.size]
        points_to_check = [(i,j) for i in filled_rows for j in filled_columns]
        
        for i,j in points_to_check:
            diag1, diag2 = get_diagonals(i,j)
            if (sum([self.get_square(i,j) != ' 'for i,j in diag1]) == len(diag1)
                and sum([self.get_square(i,j) != ' 'for i,j in diag2]) == len(diag1)):
                
                color = self.get_square(i,j)
                assert color != ' '
                sign = 1 if color == playerColor else -1
                stable_board[i][j] = sign
                checked.add((i,j))
        
        for row,col in corners:
            color = self.get_square(row,col)
            if color == playerColor:
                stable_board[row][col] = 1000
            elif color == oppColor:
                stable_board[row][col] = -1000

            if color != ' ':
                queue.extend([(row + i, col + j)
                              for i in range(-1,2)
                              for j in range(-1,2)
                              if on_board(row+i, col+j)
                              and (row+i, col+j) not in checked] )
            
        while len(queue) > 0:
            row,col = queue.pop(0)
            checked.add((row,col))
            
            color = self.get_square(row,col)
            sign = 1 if color == playerColor else -1
            
            if color == ' ' or stable_board[row][col] != 0:
                pass
            else:
                stable = True
                for i,j in self.directions[:4]:
                    if not is_stable(row + i, col + j, sign) and not is_stable(row - i, col - j, sign):
                        stable = False
                        break
                if stable:
                    stable_board[row][col] = sign
                    queue.extend([(row + i, col + j)
                                for i in range(-1,2)
                                for j in range(-1,2)
                                if on_board(row+i, col+j)
                                and (row+i, col+j) not in checked] )
        stable_score =  sum([sum(row) for row in stable_board])

        return stable_score
        
    def weighted_tile_count(self, game_over, playerColor, oppColor):
        player_score = sum([sum([self.weights[i][j] for i in range(self.size) if self.get_square(i,j) == playerColor]) for j in range(self.size)])
        opp_score = sum([sum([self.weights[i][j] for i in range(self.size) if self.get_square(i,j) == oppColor]) for j in range(self.size)])
        return player_score - opp_score

        
    def stablecount_mincount(self, game_over, playerColor, oppColor):
        score = (self.count_stable_tiles(game_over, playerColor, oppColor),
                 self.weighted_tile_count(game_over, playerColor, oppColor))

        return score

def compare_score(a,b):
    '''
    Compares two scores a and b, returning 1 if a > b, -1 if b > a, and 0 if a == b
    '''
    try:
        if a > b:
            return 1
        elif a < b:
            return -1
        else:
            return 0
    except:

        a_new = a
        b_new = b
        if type(a) in [int, float] and type(b) is tuple:
            a_new = (a,)*len(b)
        if type(b) in [int, float] and type(a) is tuple:
            b_new = (b,)*len(a)

        for score1,score2 in zip(a_new,b_new):
            if score1 > score2:
                return 1
            elif score1 < score2:
                return -1
        return 0
    
def get_max(a,b):
    '''
    Compares a and b and returns the max
    '''
    val = compare_score(a,b)

    if val > 0:
        return a
    else:
        return b

def get_min(a,b):
    '''
    Compares a and b and returns the min
    '''
    val = compare_score(a,b)

    if val < 0:
        return a
    else:
        return b
