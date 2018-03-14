'''
Serves as a testbed for game_agent

'''



from isolation import Board
from game_agent import *
from sample_players import *
import math


# player1 = MinimaxPlayer()
player2 = MinimaxPlayer()
player1 = AlphaBetaPlayer()
#player2 = AlphaBetaPlayer()

game = Board(player1, player2)
moves = game.get_legal_moves()
# for move in moves():
# 	print('move : ', move)
# 	game.forecast_move(move)

game.apply_move((3,3))
game.apply_move((3,5))

own_location = game.get_player_location(player1)
opp_location = game.get_player_location(player2)

own_moves = game.get_legal_moves(player1)
opp_moves = game.get_legal_moves(player2)


print('own_moves: ', own_moves)
print('opp_moves: ', opp_moves)


print('################')
#CUSTOM_HEURISTIC #1

own_diag_dist = 0.0

for move in own_moves:
	py_dist = math.sqrt((move[1]-opp_location[1])**2 + (move[0]-opp_location[0])**2)
	own_diag_dist += py_dist

opp_diag_dist = 0.0

for move in opp_moves:
	py_dist = math.sqrt((move[1]-own_location[1])**2 + (move[0]-own_location[0])**2)
	opp_diag_dist += py_dist

float(own_diag_dist-opp_diag_dist)


print('################')
#CUSTOM_HEURISTIC #2

close_moves = 0
for move in own_moves:
    if abs(move[0] - opp_location[0]) <= 2 and abs(move[1] - opp_location[1]) <= 2:
    	close_moves += 1

print('close moves: ', close_moves)

#CUSTOM_HEURISTIC #3

own_weights = 0.0

for move in own_moves:
    own_weights += math.sqrt((move[0]-opp_location[0])**2 + (move[1]-opp_location[1])**2)

opp_weights = 0.0
for move in opp_moves:
    opp_weights += math.sqrt((move[0]-own_location[0])**2 + (move[1]-own_location[1])**2)

print('weights: ', own_weights, ', opp_weights: ', opp_weights)



# print(game.print_board())

# print('player1 location: ', game.get_player_location(player1))
# print('player1 moves: ', game.get_legal_moves(player1))
# print('player2 location: ', game.get_player_location(player2))
# print('player2 moves: ', game.get_legal_moves(player2))

