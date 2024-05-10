import cli_input
from heuristics import Heuristics
from game import Game
import tests
from minimax import minimax_alpha_beta_puring
from halma import check_for_winner


def run_tests():
    tests.check_for_max_possible_moves_in_halma()
    tests.check_execution_time_of_algorithms_and_heuristics()
    tests.simulate_game()


def run_game(game: Game, p1_heuristics: dict, p2_heuristics: dict, depth: int = 3, rounds: int = 300):
    counter = 1
    p1_heuristic = next(iter(p1_heuristics.values()))
    p2_heuristic = next(iter(p2_heuristics.values()))
    print(f'round nr {counter}')
    game.print_colorful_board()

    while (game.winner == 0 and counter < rounds):
        game.check_for_winner(check_for_winner)
        if (game.winner != 0):
            print(f'WINNER: player {game.winner}')
            print(game)
            break 
        if (counter % 10 == 0):
            print(f'round nr {counter}')
            game.print_colorful_board()

        p1_heuristic = p1_heuristics.get(counter, p1_heuristic)
        p2_heuristic = p2_heuristics.get(counter, p2_heuristic)

        _, best_move = minimax_alpha_beta_puring(game, depth, 1, True, p1_heuristic)
        game.move_pawn(1, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        _, best_move = minimax_alpha_beta_puring(game, depth, 2, True, p2_heuristic)
        game.move_pawn(2, best_move[0], best_move[1], best_move[2][0], best_move[2][1])
        counter += 1

    

def run():
    game_state = cli_input.read_initial_game_state()
    cli_input.cli_print_initial_game_state(game_state)
    game = Game(game_state)
    player1_heuristics = {1: Heuristics.strat_dist_from_middle_diagonal, 
                          40: Heuristics.strat_dist_of_pawn_spread,
                          60: Heuristics.strat_dist_from_enemy_corner}
    player2_heuristics = {1: Heuristics.strat_dist_from_board_center,
                          50: Heuristics.strat_random,
                          70: Heuristics.strat_dist_from_furthest_pawn,
                          90: Heuristics.strat_dist_from_enemy_corner}
    # run_tests()
    run_game(game, player1_heuristics, player2_heuristics)

if __name__ == "__main__":
    run()
