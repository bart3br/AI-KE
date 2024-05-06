import math
from game import Game
from constants import MAX_NUMBER_OF_POSSIBLE_MOVES
from halma import generate_possible_player_moves

class Heuristics: 
    @staticmethod
    # heuristic taking average player's pawns distance from enemy board corner as factor
    # the lower the average distance, the higher heuristic value
    def strat_dist_from_enemy_corner(game: Game, player_num: int, enemy_corner_x: int, enemy_corner_y: int) -> float:
        MAX_DIST = euclidean_dist(0, 0, game.BOARD_SIZE, game.BOARD_SIZE)
        
        avg_dist = count_avg_distance_from_point(game, player_num, enemy_corner_x, enemy_corner_y)
        # dividing avg_dist by max_dist to get number from 0 to 1, as max_dist will always be bigger than avg_dist
        # returning 1.0 - avg_dist because the bigger the avg_dist from enemy corner, the smaller should heuristic value be
        avg_dist /= MAX_DIST
        return 1.0 - avg_dist
    
    @staticmethod
    # heuristic taking average player's pawns distance from center of the board as factor
    # the lower the average distance, the higher heuristic value            
    def strat_dist_from_board_center(game: Game, player_num: int) -> float:
        BOARD_CENTER = (game.BOARD_SIZE/2, game.BOARD_SIZE/2)
        MAX_DIST = euclidean_dist(0, 0, BOARD_CENTER[0], BOARD_CENTER[1])
        
        avg_dist = count_avg_distance_from_point(game, player_num, BOARD_CENTER[0], BOARD_CENTER[1])
        avg_dist /= MAX_DIST
        return 1.0 - avg_dist

    @staticmethod
    # heuristic taking number of possible player moves as factor
    # the higher the number of possible moves, the higher heuristic value
    def strat_number_of_possible_moves(game: Game, player_num: int) -> float:
        possible_moves_count = len(generate_possible_player_moves(game, player_num))
        possible_moves_count /= MAX_NUMBER_OF_POSSIBLE_MOVES
        return possible_moves_count if possible_moves_count < 1.0 else 1.0

    @staticmethod
    # heuristic taking average player's pawns distance from furthest player's pawn as factor
    # furthest pawn is a pawn furthest from player's start corner
    # the lower the average distance, the higher heuristic value
    def strat_dist_from_furthest_pawn(game: Game, player_num: int) -> float:
        START_CORNER = (0,0) if player_num == 1 else (game.BOARD_SIZE-1, game.BOARD_SIZE-1)
        MAX_DIST = euclidean_dist(0, 0, game.BOARD_SIZE, game.BOARD_SIZE)

        furthest_pawn = START_CORNER
        furthest_pawn_dist = 0.0
        for x in range(game.BOARD_SIZE):
            for y in range(game.BOARD_SIZE):
                if (game.get_cell_val(x,y) == player_num):
                    distance = euclidean_dist(x, y, START_CORNER[0], START_CORNER[1])
                    if (distance > furthest_pawn_dist):
                        furthest_pawn = (x, y)
                        furthest_pawn_dist = distance
        avg_dist = count_avg_distance_from_point(game, player_num, furthest_pawn[0], furthest_pawn[1])
        avg_dist /= MAX_DIST
        return 1.0 - avg_dist


    @staticmethod
    # heuristic taking player's pawns spread as factor
    # pawn spread is average distance from pawn to every other pawn
    # the lower the pawn spread, the higher heuristic value
    def strat_dist_of_pawn_spread(game: Game, player_num: int) -> float:
        MAX_DIST = euclidean_dist(0, 0, game.BOARD_SIZE, game.BOARD_SIZE)
        avg_spread_dist = 0.0
        player_pawns_coordinates = []
        for x in range(game.BOARD_SIZE):
            for y in range(game.BOARD_SIZE):
                if (game.get_cell_val(x,y) == player_num):
                    player_pawns_coordinates.append((x,y))
        for pawn in player_pawns_coordinates:
            avg_spread_dist += count_avg_distance_from_point(game, player_num, pawn[0], pawn[1])
        avg_spread_dist /= len(player_pawns_coordinates)
        avg_spread_dist /= MAX_DIST
        return 1.0 - avg_spread_dist
        

    @staticmethod
    # heuristic taking average player's pawns distance from middle diagonal of the board as factor
    # the lower the average distance, the higher heuristic value 
    def strat_dist_from_middle_diagonal(game: Game, player_num: int) -> float:
        MAX_DIST = euclidean_dist(0, 0, game.BOARD_SIZE, game.BOARD_SIZE) / 2
        DIAG_COEFF_B = -1.0
        DIAG_COEFF_A, DIAG_COEFF_C = count_linear_equation_of_line(0, game.BOARD_SIZE-1, game.BOARD_SIZE-1, 0)
        avg_dist = 0.0
        player_pawn_count = 0
        for x in range(game.BOARD_SIZE):
            for y in range(game.BOARD_SIZE):
                if (game.get_cell_val(x,y) == player_num):
                    avg_dist += count_dist_from_point_to_line(x, y, DIAG_COEFF_A, DIAG_COEFF_B, DIAG_COEFF_C)
                    player_pawn_count += 1
        avg_dist /= player_pawn_count
        avg_dist /= MAX_DIST
        return 1.0 - avg_dist


def euclidean_dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

def count_avg_distance_from_point(game: Game, player_num: int, point_x: int, point_y: int) -> float:
    avg_dist = 0.0
    player_pawn_count = 0
    for x in range(game.BOARD_SIZE):
        for y in range(game.BOARD_SIZE):
            if (game.get_cell_val(x,y) == player_num):
                avg_dist += euclidean_dist(x, y, point_x, point_y)
                player_pawn_count += 1
    return (avg_dist / player_pawn_count)

# a and b coefficients of line's linear equation
def count_linear_equation_of_line(x1: int, y1: int, x2: int, y2: int) -> tuple:
    a_coeff = (y1 - y2) / (x1 - x2)
    b_coeff = y1 - (a_coeff * x1)
    return (a_coeff, b_coeff)

# distance from point to line using it's general equation coefficients
def count_dist_from_point_to_line(point_x: int, point_y: int, a_coeff: float, b_coeff: float, c_coeff: float) -> float:
    return abs((a_coeff * point_x) + (b_coeff * point_y) + c_coeff) / math.sqrt(pow(a_coeff, 2) + pow(b_coeff, 2))

if __name__ == "__main__":
    pass
