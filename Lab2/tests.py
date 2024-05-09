from game import Game
from halma import generate_possible_player_moves, check_for_winner
import random
import traceback
from time import time
from heuristics import Heuristics
from minimax import minimax, minimax_alpha_beta_puring
from cli_input import read_initial_game_state

def check_for_max_possible_moves_in_halma() -> None:
    game_state = read_initial_game_state()
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


def test_minimax_time(game: Game, evaluate_func, depth: int = 3, rounds: int = 5):
    time_start = time()
    for _ in range(rounds):
        _, best_move = minimax(game, depth, 1, True, evaluate_func)
        game.move_pawn(1, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        # print(f'player1 moves: {best_move}')
        # print(game)
        _, best_move = minimax(game, depth, 2, True, evaluate_func)
        game.move_pawn(2, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        # print(f'player2 moves: {best_move}')
        # print(game)
    time_end = time()
    print(f'minimax time: {round(time_end-time_start, 2)}s')

def test_minimax_alpha_beta_time(game: Game, evaluate_func, depth: int = 3, rounds: int = 5):
    time_start = time()
    for _ in range(rounds):
        _, best_move = minimax_alpha_beta_puring(game, depth, 1, True, evaluate_func)
        game.move_pawn(1, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        # print(f'player1 moves: {best_move}')
        # print(game)
        _, best_move = minimax_alpha_beta_puring(game, depth, 2, True, evaluate_func)
        game.move_pawn(2, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        # print(f'player2 moves: {best_move}')
        # print(game)
    time_end = time()
    print(f'minimax with alphabeta puring time: {round(time_end-time_start, 2)}s')


def check_execution_time_of_algorithms_and_heuristics():
    game_state = read_initial_game_state()
    print('heuristic distance from enemy corner')
    game = Game(game_state)
    test_minimax_time(game, Heuristics.strat_dist_from_enemy_corner)
    game = Game(game_state)
    test_minimax_alpha_beta_time(game, Heuristics.strat_dist_from_enemy_corner)
    print('\nheuristic distance from board center')
    game = Game(game_state)
    test_minimax_time(game, Heuristics.strat_dist_from_board_center)
    game = Game(game_state)
    test_minimax_alpha_beta_time(game, Heuristics.strat_dist_from_board_center)
    print('\nheuristic distance from furthest players pawn')
    game = Game(game_state)
    test_minimax_time(game, Heuristics.strat_dist_from_furthest_pawn)
    game = Game(game_state)
    test_minimax_alpha_beta_time(game, Heuristics.strat_dist_from_furthest_pawn)
    print('\nheuristic distance of pawn spread')
    game = Game(game_state)
    test_minimax_time(game, Heuristics.strat_dist_of_pawn_spread)
    game = Game(game_state)
    test_minimax_alpha_beta_time(game, Heuristics.strat_dist_of_pawn_spread)
    print('\nheuristic distance from middle diagonal')
    game = Game(game_state)
    test_minimax_time(game, Heuristics.strat_dist_from_middle_diagonal)
    game = Game(game_state)
    test_minimax_alpha_beta_time(game, Heuristics.strat_dist_from_middle_diagonal)
    print('\nheuristic number of possible moves')
    # game = Game(game_state)
    # test_minimax_time(game, Heuristics.strat_number_of_possible_moves)
    game = Game(game_state)
    test_minimax_alpha_beta_time(game, Heuristics.strat_number_of_possible_moves)


def simulate_game_check_heuristic_and_board_state(evaluate_func, depth: int = 3, rounds: int = 1000):
    game_state = read_initial_game_state()
    game = Game(game_state)
    for i in range(rounds):
        if (check_for_winner(game) != 0):
            print(f'WINNER: player {check_for_winner(game)}')
            print(game)
            break 
        if (i % 10 == 0):
            print(f'round nr {i}')
            game.print_colorful_board()

        _, best_move = minimax_alpha_beta_puring(game, depth, 1, True, evaluate_func)
        game.move_pawn(1, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        _, best_move = minimax_alpha_beta_puring(game, depth, 2, True, evaluate_func)
        game.move_pawn(2, best_move[0], best_move[1], best_move[2][0], best_move[2][1])

def simulate_game():
    simulate_game_check_heuristic_and_board_state(Heuristics.strat_dist_from_enemy_corner)
    simulate_game_check_heuristic_and_board_state(Heuristics.strat_dist_from_board_center)
    simulate_game_check_heuristic_and_board_state(Heuristics.strat_dist_from_furthest_pawn)
    simulate_game_check_heuristic_and_board_state(Heuristics.strat_dist_of_pawn_spread)
    simulate_game_check_heuristic_and_board_state(Heuristics.strat_dist_from_middle_diagonal)
    # simulate_game_check_heuristic_and_board_state(Heuristics.strat_number_of_possible_moves)



if __name__ == "__main__":
    pass