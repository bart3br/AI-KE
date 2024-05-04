import cli_input
from halma import generate_possible_player_moves
from classes import Game, Cell

def run():
    game_state = cli_input.read_initial_game_state()
    cli_input.cli_print_initial_game_state(game_state)
    
    game = Game(game_state, 2, 19)
    print(game)
    
    print(generate_possible_player_moves(game, 1))
    

if __name__ == "__main__":
    run()
