
from copy import deepcopy

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
    return True

#checks if the pieces can be flipped and returns the flippable pieces
def get_flippable(board, size, player, row, column):
    brd = deepcopy(board)
    brd[row][column] = player
    opponent = BLACK if player == WHITE else WHITE
    toFlip = []
    for rdr, cdr in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        r, c = row, column
        r += rdr
        c += cdr
        
        if is_onboard(size,r, c) and board[r][c] == opponent:
            r += rdr
            c += cdr
            if not is_onboard(size,r, c): #Check if it is a corner piece
                continue
            while board[r][c] == opponent:
                r += rdr
                c += cdr
                if not is_onboard(size,r, c): #keep checking and break if boundary is reached before finding a piece
                    break
            if not is_onboard(size,r, c): #because the break inside the while loop doesn't effect for loop
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


def flip(board, row, col, player, toBeFlipped):
    board[row][col] = player
    print(row, col)
    if len(toBeFlipped) > 0:
        for r, c in toBeFlipped:
            board[r][c] = player
        return True
    return False

#makes move
def make_move(board, size, row, column, player):
    if is_onboard(size, row, column) == False or board[row][column] != EMPTY:
        return False
    toBeFlipped = get_flippable(board, size, player, row, column)
    if toBeFlipped == False:
        return False
    flip(board, row, column, player, toBeFlipped)
    return True

def score(board, size, player):
    count = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == player:
                count = count + 1
    return count

#If there are zero flippable pieces or is out of range, returns false
def is_valid_move(board, size, row, col, player):
    if is_in_range(board, size, row, col) == False:
        return False
    toBeFlipped = get_flippable(board, size, player, row, col)
    if toBeFlipped == False:
        return False
    else:
        return True

#Gets all the legal moves for a particular player's turn
def get_legal_moves(board,size, player):
    legal_moves=[]
    for i in range(size):
        for j in range(size):
            if is_valid_move(board, size, i, j, player):
                legal_moves.append((i , j))
    return legal_moves

def has_valid_move(board, size, player):
    return len(get_legal_moves(board, size, player)) > 0

def game_over(board, size, player):
    opponent = WHITE if player == BLACK else BLACK
    if has_valid_move(board, size, player) or has_valid_move(board, size, opponent):
        return False
    else:
        return True

def get_move(board, size, player):
    print player, "'s turn\n"
    row = input("Enter row: ")
    col = input("Enter column: ")
    while not is_valid_move(board, size, row, col, player):
        print "Invalid Move! Please enter again"
        row = input("Enter row: ")
        col = input("Enter column: ")
    make_move(board, size, row, col, player)

def play_game(board, size, turn=WHITE):
    opponent = BLACK if turn == WHITE else BLACK
    while not game_over(board,size, turn):
        if has_valid_move(board, size, turn):
            get_move(board, size, turn)
        else:
            print ("No valid moves")
        print_board(board, size)
        opponent, turn = turn, opponent

    print("Game Over!")

    white_score = score(board,size, WHITE)
    black_score = score(board,size, BLACK)
    print("White:", white_score)
    print("Black:", black_score)
    if white_score > black_score:
        print("Winner: WHITE")
    elif white_score < black_score:
        print("WINNER: BLACK")
    else:
        print("TIE")

if __name__ == '__main__':
    size = int(input("Enter Size: "))
    board = init_board(size)
    print_board(board, size)
    player = WHITE
    play_game(board, size, player)
    
    