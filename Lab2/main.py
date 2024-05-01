import cli_input
from halma import is_direct_pawn_move_possible
from classes import Game, Cell

def run():
    game_state = cli_input.read_initial_game_state()
    cli_input.cli_print_initial_game_state(game_state)
    
    # pos_x = 3
    # pos_y = 2
    # print(is_direct_pawn_move_possible(game_state, pos_x, pos_y, 3, 2))
    # print(is_direct_pawn_move_possible(game_state, pos_x, pos_y, 3, 3))
    # print(is_direct_pawn_move_possible(game_state, pos_x, pos_y, 3, 4))
    # print(is_direct_pawn_move_possible(game_state, pos_x, pos_y, 2, 4))
    # print(is_direct_pawn_move_possible(game_state, pos_x, pos_y, 2, 3))
    # print(is_direct_pawn_move_possible(game_state, pos_x, pos_y, 2, 2))
    # print(is_direct_pawn_move_possible(game_state, pos_x, pos_y, 5, 2))
    game = Game(game_state, 2, 19)
    print(game)
    

if __name__ == "__main__":
    run()
