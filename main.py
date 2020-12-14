
from copy import deepcopy
import random 

EMPTY = ' '
BLACK = 'B'
WHITE = 'W'

max_closed_list={}
min_closed_list={}

def compressing(board):
    ret = ''
    for i in board:
        ret += ''.join(i)
    return ret

board6 = [[100, -30, 2, 2, -30, 100], \
          [-30, -40, -1, -1, -40, -30], \
          [2, -1, 1, 1, -1, 2],\
          [2, -1, 1, 1, -1, 2],\
          [-30, -40, 2, 2, -40, -30], \
          [100, -30, -1, -1, -30, 100]]

board8 = [[100, -30, 2, 2, 2, 2, -30, 100], \
        [-30, -40, -10, -10, -10, -10, -40, -30], \
        [2, -10, 1, 0, 0, 1, -10, 2],\
        [2, -10, 0, 1, 1, 0, -10, 2],\
        [2, -10, 0, 1, 1, 0, -10, 2],\
        [2, -10, 1, 0, 0, 1, -10, 2],\
        [-30, -40, -10, -10, -10, -10, -40, -30], \
        [100, -30, 2, 2, 2, 2, -30, 100]]
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


#Flips the flippable pieces
def flip(board, row, col, player, toBeFlipped):
    board[row][col] = player
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

#Returns the total score of a player
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

#checks if the move is valid
def has_valid_move(board, size, player):
    return len(get_legal_moves(board, size, player)) > 0

#returns true if both players do not have any valid moves to make
def game_over(board, size, player):
    opponent = WHITE if player == BLACK else BLACK
    if has_valid_move(board, size, player) or has_valid_move(board, size, opponent):
        return False
    else:
        return True

#gets move from the player
def get_move(board, size, player):
    print player, "'s turn\n"
    row = input("Enter row: ")
    col = input("Enter column: ")
    while not is_valid_move(board, size, row, col, player):
        print "Invalid Move! Please enter again"
        row = input("Enter row: ")
        col = input("Enter column: ")
    make_move(board, size, row, col, player)
####################################################################### 

######################### MAIN GAME ####################################

#runs a loop till game is over
def play_game(board, size, turn=WHITE):
    opponent = BLACK if turn == WHITE else BLACK
    while not game_over(board,size, turn):
        if turn == WHITE:
            print("WHITE's turn...")
            if has_valid_move(board, size, turn):
                move = random_move(board, size, turn)
                print "move: ", move
                make_move(board, size, move[0], move[1], turn)
                #get_move(board, size, turn)
            else:
                print ("No valid moves")
        else:
            print("BLACK's turn...")
            move = calculate(board, size, turn)
            print "move: ", move
            make_move(board, size, move[0], move[1], turn)
            
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




############## HEURISTICS ######################################

def mobility(board, size, player):
        opponent = BLACK if player == WHITE else WHITE
        player_moves = len(get_legal_moves(board, size, player))
        opponent_moves = len(get_legal_moves(board, size, opponent))
        return 100 * (player_moves - opponent_moves)

def corners_captured(board, size, player):
    opponent = BLACK if player == WHITE else WHITE
    player_corners = 0
    opponent_corners = 0
    for i, j in ((0,0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)):
        if board[i][j] == player:
            player_corners += 1
        elif board[i][j] == opponent:
            opponent_corners += 1
    return 100 * (player_corners - opponent_corners)

def get_move_weight(board, size, player):
    opponent = BLACK if player == WHITE else WHITE
    player_score = 0
    opponent_score = 0
    player_moves = get_legal_moves(board, size, player)
    opponent_moves = get_legal_moves(board, size, opponent)
    if size == 6:
        for i, j in player_moves:
            player_score += board6[i][j]
        for i, j in opponent_moves:
            opponent_score += board6[i][j]
    elif size == 8:
        for i, j in player_moves:
            player_score += board8[i][j]
        for i, j in opponent_moves:
            opponent_score += board8[i][j]
    else:
        return 0
    return player_score - opponent_score

def heuristic(board, size, player):
    mob = mobility(board, size, player)
    cor = corners_captured(board, size, player)
    weight = get_move_weight(board, size, player)
    # print "Mobility: ", mob
    # print "Corner Score: ", cor
    return mob + cor + weight

def random_move(board, size, player):
        moves = get_legal_moves(board,size,player)
        if len(moves) == 0:
            return (-1, -1)
        else:
            i = random.choice(moves)
            return i
################################################################
def max(a, b):
    return a if a >= b else b

def min(a, b):
    return a if a <= b else b


def result(board, size, move, player):
    new_board = deepcopy(board)
    make_move(new_board, size, move[0], move[1], player)
    return new_board



def calculate(board, size, player):
    opponent = BLACK if player == WHITE else WHITE
    value, final_move = alphabeta(board, size, player, opponent, 6, -100000000, 100000000, True)
    max_closed_list.clear
    min_closed_list.clear
    return final_move


def alphabeta(board, size, player, opponent, depth, alpha, beta, isMaximizing):
    if depth == 0:
        return heuristic(board, size, player), [-1000, -1000]
        
    if isMaximizing:
        value = -10000000
        final_move = None
        movelist = get_legal_moves(board,size, player)
        if len(movelist) < 1:
            value = heuristic(board, size, player)
        for move in movelist:
            s1 = result(board, size, move, player)
            compressed = compressing(s1)
            if compressed in max_closed_list:
                return max_closed_list[compressed][0], max_closed_list[compressed][1] 
            new_value, new_move = alphabeta(s1, size, player, opponent, depth - 1, alpha, beta, False)
            if value <= new_value:
                value = new_value
                final_move = move
            alpha = max(alpha, value)
            max_closed_list[compressed] = alpha, final_move
            if alpha >= beta:
                break
                
        return value, final_move
    else:
        value = 10000000
        final_move = None
        movelist = get_legal_moves(board, size, opponent)
        if len(movelist) < 1:
            value = heuristic(board, size, player)
        for move in movelist:
            s1 = result(board, size, move, opponent)
            compressed = compressing(s1)
            if compressed in min_closed_list:
                #print min_closed_list[compressed][0], min_closed_list[compressed][1]
                return min_closed_list[compressed][0], min_closed_list[compressed][1] 
            new_value, new_move = alphabeta(s1, size, player, opponent, depth - 1, alpha, beta, True)
            if value >= new_value:
                value = new_value
                final_move = move
            beta = min(beta, value)
            min_closed_list[compressed] = beta, final_move
            if alpha >= beta:
                break
        return value, final_move

####################################################################
if __name__ == '__main__':
    size = int(input("Enter Size: "))
    board = init_board(size)
    print_board(board, size)
    player = WHITE
    play_game(board, size, player)
    
####################################################################### 
