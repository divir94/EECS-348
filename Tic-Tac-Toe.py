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
                

def minimax(board, depth, maximizingPlayer):
    #print board
    if board.winner() == 'X': return 1, (-2,-2) # I guess the return move (-2,-2) doesn't matter
    elif board.winner() == 'O': return -1, (-2,-2)
    elif depth == 0 or board.full_board(): return 0, (-2,-2)

    if maximizingPlayer:
        bestValue = float("-inf")
        bestMove = (-1,-1)
        for i in range(3):
            for j in range(3):
                if board.get_square(i,j) == 'N':
                    board.play_square(i,j,'X')
                    val, (besti, bestj) = minimax(board, depth-1, False)
                    # update bestValue 
                    if val > bestValue:
                        bestValue = val
                        bestMove = (i,j)
                    board.play_square(i,j,'N')
        return bestValue, bestMove
    else:
        bestValue = float("inf")
        for i in range(3):
            for j in range(3):
                if board.get_square(i,j) == 'N':
                    board.play_square(i,j,'O')
                    val, (besti, bestj) = minimax(board, depth-1, True)
                    # update bestValue 
                    if val < bestValue:
                        bestValue = val
                        bestMove = (i,j)
                    board.play_square(i,j,'N')
        return bestValue, bestMove

    
    

def play():
    Board = TicTacToeBoard()
    humanval =  'X'
    cpuval = 'O'
    depth = 7 # Number of moves to look ahead
    print Board
    
    while( Board.full_board()==False and Board.winner() == 'N'):
        print "your move, pick a row and column (0-2)"
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
                bestValue, bestMove = minimax(Board, depth, False)
                Board.play_square(bestMove[0], bestMove[1], cpuval)
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
