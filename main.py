
EMPTY = ' '
BLACK = 'B'
WHITE = 'W'


######################### INITIALIZATION OF BOARD ##################
def init_board(size):
    mid = size/2
    board = []
    for i in range(size):
        board.append([EMPTY] * size)
    board[mid - 1][mid - 1] = BLACK
    board[mid - 1][mid] = WHITE
    board[mid][mid-1] = WHITE
    board[mid][mid] = BLACK
    return board
######################################################################    


############################# DRAWING BOARD########################### 

def draw_row(size):
    ret = ' '
    for column in range(size):
        ret += '+-'
    ret += '+\n'
    return ret

def draw_col(size, board, row):
    ret = str(row)
    ret += '|'
    for column in range(size):
        ret += board[row][column]
        ret += '|'
    ret += '\n'
    return ret

def print_board(board, size):
    ret = ' '
    for column in range(size):
        ret += " " + str(column)
    ret+= '\n'
    for row in range(size):
        ret += draw_row(size)
        ret += draw_col(size, board, row)
    ret += draw_row(size)
    print ret
####################################################################### 


############################ MAKING MOVE ############################## 

def is_onboard(size, row, col):
    return row >= 0 and row < size and col >= 0 and col < size
 
def is_in_range(board, size, row, col): #check if is on board and is empty
    if is_onboard(size, row, col) == False or board[row][col] != EMPTY:
        return False

#checks if the pieces can be flipped and returns the flippable pieces
def get_flippable(board, player, row, column):
    brd = deepcopy(board)
    brd[row][column] = player
    opponent = BLACK if player == WHITE else WHITE
    toFlip = []
    for ro, cl in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        r, c = row, column
        r += rdr
        c += cdr
        
        if is_onboard(r, c) and board[r][c] == opponent:
            r += rdr
            c += cdr
            if not is_onboard(r, c): #Check if it is a corner piece
                continue
            while board[r][c] == opponent:
                r += rdr
                c += cdr
                if not is_onboard(r, c): #keep checking and break if boundary is reached before finding a piece
                    break
            if not is_onboard(r, c): #because the break inside the while loop doesn't effect for loop
                continue
            if brd[r][c] == player:
                while True:
                    r -= rdr
                    c -= cdr
                    if r == row and c == column:
                        break
                    toFlip.append([r, c])
    del brd
    if len(toFlip) == 0:
        return False
    return toFlip


    def flip(self,board, row, col, player, toBeFlipped):
        board[row][col] = player
        print(row, col)
        if len(toBeFlipped) > 0:
            for r, c in toBeFlipped:
                board[r][c] = player
            return True
        return False

    #makes move
    def make_move(board, row, column, player):
        if is_onboard(row, column) == False or board[row][column] != EMPTY:
            return False
        toBeFlipped = get_flippable(board, player, row, column)
        if toBeFlipped == False:
            return False
        flip(row, column, player, toBeFlipped)
        return True
    
    def score(board, size, player):
        count = 0
        for i in range(size):
            for j in range(size):
                if board[i][j] == player:
                    count = count + 1
        return count

if __name__ == '__main__':
    n = input("Please enter size: ")
    board = init_board(n)
    
    print_board(board, n)
    
    