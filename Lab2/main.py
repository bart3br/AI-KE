import cli_input
from heuristics import Heuristics
from game import Game
from node import Node
from tests import check_for_max_possible_moves_in_halma
from minimax import minimax
from time import time

from copy import deepcopy
from halma import generate_possible_player_moves

def run():
    game_state = cli_input.read_initial_game_state()
    cli_input.cli_print_initial_game_state(game_state)
    # check_for_max_possible_moves_in_halma(game_state)
    
    game = Game(game_state)
    print(game)
    # run_minimax(game)
    # time1 = time()
    for _ in range(10):
        _, best_move = minimax(game, 3, 1, True, Heuristics.strat_dist_from_board_center)
        game.move_pawn(1, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        print(best_move)
        print(game)
    # time2 = time()
    # print(f'time:{round(time2 - time1, 2)}s')
    # print(f'best move: {best_move}')
    
def run_minimax(game: Game):
    for _ in range(10):
        _, best_move = minimax(game, 3, 1, True, Heuristics.strat_dist_from_enemy_corner)
        game.move_pawn(1, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        print(best_move)
        print(game)
        _, best_move = minimax(game, 3, 2, True, Heuristics.strat_dist_from_enemy_corner)
        game.move_pawn(2, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        print(best_move)
        print(game)
    

if __name__ == "__main__":
    run()
