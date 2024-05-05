from game import Game
from halma import generate_possible_player_moves
import random
import traceback

def check_for_max_possible_moves_in_halma(game_state: list) -> None:
    NUMBER_OF_GAMES = 100

    turns_without_error_played = 0
    min_number_of_possible_moves = 0
    avg_number_of_possible_moves = 0
    max_number_of_possible_moves = 0
    for _ in range(NUMBER_OF_GAMES):
        game = Game(game_state)
        player_num_turn = 1
        min_moves = 0
        avg_moves = 0
        max_moves = 0
        for _ in range(10000):
            player_num_turn = 2 if game.turn % 2 == 0 else 1
            possible_moves = generate_possible_player_moves(game, player_num_turn)
            
            if (len(possible_moves) < min_moves):
                min_moves = len(possible_moves)
            if (len(possible_moves) > max_moves):
                max_moves = len(possible_moves)
            avg_moves += len(possible_moves)
            
            chosen_move = random.choice(possible_moves)
            try:
                game.move_pawn(player_num_turn, chosen_move[0], chosen_move[1], (chosen_move[2])[0], (chosen_move[2])[1])
            except:
                traceback.print_exc()
                print(game)
                print(chosen_move)
        avg_moves /= (game.turn - 1)

        turns_without_error_played += game.turn - 1
        min_number_of_possible_moves = min_moves if min_moves < min_number_of_possible_moves else min_number_of_possible_moves
        avg_number_of_possible_moves += avg_moves
        max_number_of_possible_moves = max_moves if max_moves > max_number_of_possible_moves else max_number_of_possible_moves
    avg_number_of_possible_moves /= NUMBER_OF_GAMES
    print(f'number of turns without error played: {turns_without_error_played}')
    print(f'min number of possible moves during the game: {min_number_of_possible_moves}')
    print(f'avg number of possible moves during the game: {avg_number_of_possible_moves}')
    print(f'max number of possible moves during the game: {max_number_of_possible_moves}')

if __name__ == "__main__":
    pass