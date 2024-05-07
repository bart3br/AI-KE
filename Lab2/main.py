import cli_input
from heuristics import Heuristics
from game import Game
from node import Node
from tests import check_for_max_possible_moves_in_halma
from minimax import minimax, minimax2

from copy import deepcopy
from halma import generate_possible_player_moves

def run():
    game_state = cli_input.read_initial_game_state()
    cli_input.cli_print_initial_game_state(game_state)
    # print(game)
    # print(generate_possible_player_moves(game, 1))
    # print(strat_dist_from_enemy_corner(game, 1, game.BOARD_SIZE-1, game.BOARD_SIZE-1))
    # check_for_max_possible_moves_in_halma(game_state)
    game = Game(game_state)
    _, best_move = minimax2(game, 3, 1, True, Heuristics.strat_dist_from_enemy_corner)
    print(f'best move: {best_move}')
    

if __name__ == "__main__":
    run()
