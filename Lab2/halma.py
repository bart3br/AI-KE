from classes import Game, Cell
    
def generate_possible_player_moves(game: Game, player: int) -> list:
    pass

def generate_possible_pawn_moves(game: Game, pos_x: int, pos_y: int):
    pass

# checks if direct (single) move from current pawn position to another is possible
# a direct (single) move is a move to free neighbour cell or jumping over 1 pawn into a free cell
def is_direct_pawn_move_possible(game: Game, pos_x: int, pos_y: int, target_pos_x: int, target_pos_y: int) -> bool:
    # target cell is outside the board
    if (not is_position_inside_board(game, target_pos_x, target_pos_y)):
        return False
    # target cell is not empty (there is a pawn already)
    if (game.get_cell_val(target_pos_x, target_pos_y) != 0):
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
    if (pos_x >= len(game.board) or pos_y >= len(game.board[0])):
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
    return game.get_cell_val(jump_over_pos_x, jump_over_pos_y) == 0
     
    
if __name__ == "__main__":
    pass