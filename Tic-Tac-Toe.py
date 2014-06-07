from time import time

class TicTacToeBoard:
    def __init__(self):
        self.board = ([' ']*3,[' ']*3,[' ']*3)
                                      
    def play_square(self, row, col, val):
        self.board[row][col] = val

    def get_square(self, row, col):
        return self.board[row][col]

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if(self.board[i][j]==' '):
                    return False

        return True
    
    #if there is a winner this will return their symbol (either 'X' or 'O'),
    #otherwise it will return ' '
    def winner(self):
        #check the cols
        for col in range(3):
            if(self.board[col][0]!=' ' and self.board[col][0] == self.board[col][1] and self.board[col][0]==self.board[col][2] ):
                return self.board[col][0]
            
        #check the rows
        for row in range(3):
            if(self.board[0][row]!=' ' and self.board[0][row] == self.board[1][row] and self.board[0][row]==self.board[2][row] ):
                return self.board[0][row]

        #check diagonals
        if(self.board[0][0]!=' ' and self.board[0][0] == self.board[1][1] == self.board[2][2] ):
            return self.board[0][0]
        if(self.board[0][2]!=' ' and self.board[0][2] == self.board[1][1] == self.board[2][0] ):
            return self.board[0][2]
        return ' '

    def __repr__(self):
        s = '\n-----\n'
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                s +=  str(self.get_square(i,j)) + '|'
            s += '\n-----\n'
        return s

    
def minimax(board, maximizingPlayer, pruning, alpha, beta, depth, count):
    # base case
    # return values are (payoff, (bestMove_i, bestMove_j), count)
    if board.winner() == 'X': return 1, (-2,-2), count # I guess the return move (-2,-2) doesn't matter
    elif board.winner() == 'O': return -1, (-2,-2), count
    elif depth == 0 or board.full_board(): return 0, (-2,-2), count

    bestMove = (-1,-1)
    symbol = {True: 'X', False: 'O'} # maximizing player has 'X' and minimizing 'O'
    
    for i in range(3):
        for j in range(3):
            if board.get_square(i,j) == ' ': # if square not taken
                board.play_square(i,j, symbol[maximizingPlayer] ) # try value
                val, (bestMove_i, bestMove_j), count = minimax(board, not maximizingPlayer, pruning, alpha, beta, depth-1, count+1)
                board.play_square(i,j,' ') # restore value
                # update bestValue and bestMove
                if maximizingPlayer:
                    if val > alpha:
                        alpha = val
                        bestMove = (i,j)
                else:
                    if val < beta:
                        beta = val
                        bestMove = (i,j)
                # if pruning, avoid unnecessary banches
                if pruning and beta <= alpha: break

    if maximizingPlayer: return alpha, bestMove, count
    return beta, bestMove, count

def minimax(board, depth, maximizingPlayer):
    #print board
    if board.winner() == 'X': return 1, (-2,-2) # I guess the return move (-2,-2) doesn't matter
    elif board.winner() == 'O': return -1, (-2,-2)
    elif depth == 0 or board.full_board(): return 0, (-2,-2)

    bestMove = (-1,-1)
    if maximizingPlayer:
        bestValue = float("-inf")
        for i in range(3):
            for j in range(3):
                if board.get_square(i,j) == ' ':
                    board.play_square(i,j,'X')
                    val, (besti, bestj) = minimax(board, depth-1, False)
                    # update bestValue 
                    if val > bestValue:
                        bestValue = val
                        bestMove = (i,j)
                    board.play_square(i,j,' ')
        return bestValue, bestMove
    else:
        bestValue = float("inf")
        for i in range(3):
            for j in range(3):
                if board.get_square(i,j) == ' ':
                    board.play_square(i,j,'O')
                    val, (besti, bestj) = minimax(board, depth-1, True)
                    # update bestValue 
                    if val < bestValue:
                        bestValue = val
                        bestMove = (i,j)
                    board.play_square(i,j,' ')
        return bestValue, bestMove
    
def makeMove(Board, depth, cpuval):
    print "CPU Move"
    start_time = time() # record time
    #bestValue, bestMove, count = minimax(Board, cpuval=='X', True, float("-Inf"), float("Inf"), depth, 0)
    bestValue, bestMove = minimax(Board, depth, cpuval=='X')
    elapsed_time = time() - start_time
    Board.play_square(bestMove[0], bestMove[1], cpuval) # play move
    print "Number of nodes searched: %d \nTime taken: %.2f" % (0, elapsed_time)


def play():
    Board = TicTacToeBoard()
    humanval =  'X'
    cpuval = 'O'
    depth = 9 # Number of moves to look ahead

    if cpuval=='X':
        makeMove(Board, depth, cpuval)

    # keep playing while board is not full and there is no winner
    while( Board.full_board()==False and Board.winner() == ' '):
        print Board
        print "your move, pick a row, column e.g. 0,2"
        row, col = input()
        row, col = int(row), int(col)

        if(Board.get_square(row,col)!=' '): # check for free square
            print "square already taken!"
            continue
        else:
            Board.play_square(row,col,humanval)
            if(Board.full_board() or Board.winner()!=' '):
                break
            else:
                makeMove(Board, depth, cpuval)

    print Board
    if(Board.winner()==' '):
        print "Cat game" 
    elif(Board.winner()==humanval):
        print "You Win!"
    elif(Board.winner()==cpuval):
        print "CPU Wins!"

def main():
    play()

main()
