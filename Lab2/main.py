import cli_input
from heuristics import Heuristics
from game import Game
from tests import check_for_max_possible_moves_in_halma

def run():
    game_state = cli_input.read_initial_game_state()
    cli_input.cli_print_initial_game_state(game_state)
    # print(game)
    
    # print(generate_possible_player_moves(game, 1))
    # print(strat_dist_from_enemy_corner(game, 1, game.BOARD_SIZE-1, game.BOARD_SIZE-1))
    check_for_max_possible_moves_in_halma(game_state)

if __name__ == "__main__":
    run()
