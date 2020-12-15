from main import *

def get_winner(board_state):
    black_score = 0
    white_score = 0
    for row in board_state:
        for col in row:
            if col == 'W':
                white_score += 1
            elif col == 'B':
            	black_score += 1
    if black_score > white_score:
        winner = 'B'
    elif white_score > black_score:
        winner = 'W'
    else:
        winner = None
    return (winner, white_score, black_score)


def prepare_next_turn(turn, white_get_move, black_get_move):
    next_turn = 'W' if turn == 'B' else 'B'
    next_move_function = white_get_move if next_turn == 'W' else black_get_move
    return next_turn, next_move_function


def print_board(board_state):
    for row in board_state:
        print row
   	 

def simulate_game(board_state,
                  board_size,
                  white_get_move,
                  black_get_move):
    player_blocked = False
    turn = 'B'
    get_move = black_get_move
    print_board(board_state)
    
    while True:
        ## GET ACTION ##
        next_action = get_move(board_size=board_size,
                               board_state=board_state,
                               turn=turn,
                               time_left=0,
                               opponent_time_left=0)
    	print "turn: ", turn, "next action: ", next_action
    	_ = raw_input()

    	## CHECK FOR BLOCKED PLAYER ##
    	if next_action is None:
            if player_blocked:
            	print "Both players blocked!"
            	break
            else:
                player_blocked = True
                turn, get_move = prepare_next_turn(turn, white_get_move, black_get_move)
            	continue
    	else:
            player_blocked = False

    	## APPLY ACTION ##
    	## Replace this function with your own apply function
    	board_state = main.apply_action(board_state=board_state,
                                    	action=next_action,
                                    	turn=turn)
    	print_board(board_state)
    	turn, get_move = prepare_next_turn(turn, white_get_move, black_get_move)
        
	winner, white_score, black_score = get_winner(board_state)
        
	print "Winner: ", winner
	print "White score: ", white_score
	print "Black score: ", black_score
    

if __name__ == "__main__":
    ## Replace with whatever board size you want to run on
    board_state = [[' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' '],
               	   [' ', ' ', 'W', 'B', ' ', ' '],
               	   [' ', ' ', 'B', 'W', ' ', ' '],
               	   [' ', ' ', ' ', ' ', ' ', ' '],
                   [' ', ' ', ' ', ' ', ' ', ' ']]
    board_size = 6

	## Give these the get_move functions from whatever ais you want to test
    white_get_move = play_game(board_state, board_size, 'W')
    black_get_move = play_game(board_state, board_size, 'B')
    simulate_game(board_state, board_size, white_get_move, black_get_move)
