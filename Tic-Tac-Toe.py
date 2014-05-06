from time import time

class TicTacToeBoard:

    def __init__(self):
        self.board = (['N']*3,['N']*3,['N']*3)
                                      
    def play_square(self, row, col, val):
        self.board[row][col] = val

    def get_square(self, row, col):
        return self.board[row][col]

    def full_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if(self.board[i][j]=='N'):
                    return False

        return True
    
    #if there is a winner this will return their symbol (either 'X' or 'O'),
    #otherwise it will return 'N'
    def winner(self):
        #check the cols
        for col in range(3):
            if(self.board[col][0]!='N' and self.board[col][0] == self.board[col][1] and self.board[col][0]==self.board[col][2] ):
                return self.board[col][0]
            
        #check the rows
        for row in range(3):
            if(self.board[0][row]!='N' and self.board[0][row] == self.board[1][row] and self.board[0][row]==self.board[2][row] ):
                return self.board[0][row]

        #check diagonals
        if(self.board[0][0]!='N' and self.board[0][0] == self.board[1][1] == self.board[2][2] ):
            return self.board[0][0]
        if(self.board[0][2]!='N' and self.board[0][2] == self.board[1][1] == self.board[2][0] ):
            return self.board[0][2]
        return 'N'

    def __repr__(self):
        s = '\n-----\n'
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                s +=  str(self.get_square(i,j)) + '|'
            s += '\n-----\n'
        return s

    
def minimax(board, depth, alpha, beta, maximizingPlayer, count, pruning):
    # base case
    if board.winner() == 'X': return 1, (-2,-2), count # I guess the return move (-2,-2) doesn't matter
    elif board.winner() == 'O': return -1, (-2,-2), count
    elif depth == 0 or board.full_board(): return 0, (-2,-2), count

    bestMove = (-1,-1)
    
    if maximizingPlayer:
        for i in range(3):
            for j in range(3):
                if board.get_square(i,j) == 'N':
                    board.play_square(i,j,'X') # try value
                    val, (besti, bestj), count = minimax(board, depth-1, alpha, beta, False, count+1, pruning)
                    board.play_square(i,j,'N') # restore value
                    # update bestValue 
                    if val > alpha:
                        alpha = val
                        bestMove = (i,j)
                    if pruning:
                        if beta <= alpha:   break
                    
        return alpha, bestMove, count
    
    else:        
        for i in range(3):
            for j in range(3):
                if board.get_square(i,j) == 'N':
                    board.play_square(i,j,'O')
                    val, (besti, bestj), count = minimax(board, depth-1, alpha, beta, True, count+1, pruning)
                    board.play_square(i,j,'N')
                    # update bestValue 
                    if val < beta:
                        beta = val
                        bestMove = (i,j)
                    if pruning:
                        if beta <= alpha:   break
                    
        return beta, bestMove, count
    

def play():
    Board = TicTacToeBoard()
    humanval =  'X'
    cpuval = 'O'
    depth = 9 # Number of moves to look ahead
    print Board
    
    while( Board.full_board()==False and Board.winner() == 'N'):
        print "your move, pick a row, column (0-2) e.g. 0,2"
        row, col = input()
        row, col = int(row), int(col)

        if(Board.get_square(row,col)!='N'):
            print "square already taken!"
            continue
        else:
            Board.play_square(row,col,humanval)
            if(Board.full_board() or Board.winner()!='N'):
                break
            else:
                print Board
                print "CPU Move"
                start_time = time()
                bestValue, bestMove, count = minimax(Board, depth, float("-Inf"), float("Inf"), False, 0, True)
                elapsed_time = time() - start_time
                Board.play_square(bestMove[0], bestMove[1], cpuval)
                print "Number of nodes searched: %d \nTime taken: %.2f" % (count, elapsed_time)
                print Board

    print Board
    if(Board.winner()=='N'):
        print "Cat game" 
    elif(Board.winner()==humanval):
        print "You Win!"
    elif(Board.winner()==cpuval):
        print "CPU Wins!"

def main():
    play()

main()
