from game import Game
from constants import POSSIBLE_PAWN_MOVES, POSSIBLE_PAWN_JUMPS, EMPTY_CELL_VALUE
from constants import PLAYER1_STARTING_CELLS, PLAYER2_STARTING_CELLS
    
def is_player_win(game: Game, player_num: int) -> bool:
    ENEMY_CORNER_CELLS = PLAYER1_STARTING_CELLS if player_num == 2 else PLAYER2_STARTING_CELLS
    for position in ENEMY_CORNER_CELLS:
        if (game.get_cell_val(position[0], position[1]) != player_num):
            return False
    return True

def generate_possible_player_moves(game: Game, player_num: int) -> list[tuple]:
    return [(x, y, move)
            for x in range(game.BOARD_SIZE)
            for y in range(game.BOARD_SIZE)
            if (game.get_cell_val(x, y) == player_num)
            for move in generate_possible_pawn_moves(game, x, y)]
                

def generate_possible_pawn_moves(game: Game, pos_x: int, pos_y: int) -> list[tuple]:
    candidate_moves = [(pos_x + move[0], pos_y + move[1]) for move in POSSIBLE_PAWN_MOVES]
    possible_moves = []
    for move in candidate_moves:
        if (is_direct_pawn_move_possible(game, pos_x, pos_y, move[0], move[1])):
            possible_moves.append(move)
    possible_moves.extend(generate_possible_pawn_jumps(game, pos_x, pos_y, []))
    # possible_moves can have duplicate moves
    # because a sequence of jumps could lead to a starting cell's direct neigbour
    return list(set(possible_moves))

def generate_possible_pawn_jumps(game: Game, pos_x: int, pos_y: int, visited_cells: list[tuple]) -> list[tuple]:
    candidate_jumps = [(pos_x + move[0], pos_y + move[1]) for move in POSSIBLE_PAWN_JUMPS]
    candidate_jumps = list(filter(lambda move: move not in visited_cells, candidate_jumps))
    
    possible_jumps = []
    for move in candidate_jumps:
        if (is_direct_pawn_move_possible(game, pos_x, pos_y, move[0], move[1])):
            possible_jumps.append(move)
            visited_cells.append(move)
            possible_jumps.extend(generate_possible_pawn_jumps(game, move[0], move[1], visited_cells))
    return list(possible_jumps)        

# checks if direct (single) move from current pawn position to another is possible
# a direct (single) move is a move to free neighbour cell or jumping over 1 pawn into a free cell
def is_direct_pawn_move_possible(game: Game, pos_x: int, pos_y: int, target_pos_x: int, target_pos_y: int) -> bool:
    # target cell is outside the board
    if (not is_position_inside_board(game, target_pos_x, target_pos_y)):
        return False
    # target cell is not empty (there is a pawn already)
    if (game.get_cell_val(target_pos_x, target_pos_y) != EMPTY_CELL_VALUE):
        return False
    
    dist_x = abs(pos_x - target_pos_x)
    dist_y = abs(pos_y - target_pos_y)
    # move requires moving more than 2 rows/columns so it's not direct move
    if (dist_x > 2 or dist_y > 2):
        return False
    # target cell is the same as current cell
    if (dist_x == 0 and dist_y == 0):
        return False
    # target cell is direct neighbour to current cell
    if (dist_x < 2 and dist_y < 2):
        return True
    # target cell isn't direct neighbour to current cell
    # it requires jumping
    return is_jump_possible(game, pos_x, pos_y, target_pos_x, target_pos_y)
    
    
def is_position_inside_board(game: Game, pos_x: int, pos_y: int):
    if (pos_x < 0 or pos_y < 0):
        return False
    if (pos_x >= game.BOARD_SIZE or pos_y >= game.BOARD_SIZE):
        return False
    return True


def is_jump_possible(game: Game, pos_x: int, pos_y: int, target_pos_x: int, target_pos_y: int):
    dist_x = abs(pos_x - target_pos_x)
    dist_y = abs(pos_y - target_pos_y)
    if (dist_x != 2 and dist_y != 2):
        return False
    # jump is not by diagonal, nor up, down, left or right
    # therefore it's forbidden
    if ((pos_x + target_pos_x) % 2 != 0 or (pos_y + target_pos_y) % 2 != 0):
        return False
    
    jump_over_pos_x = (pos_x + target_pos_x) // 2
    jump_over_pos_y = (pos_y + target_pos_y) // 2
    return game.get_cell_val(jump_over_pos_x, jump_over_pos_y) != EMPTY_CELL_VALUE
     
    
if __name__ == "__main__":
    pass