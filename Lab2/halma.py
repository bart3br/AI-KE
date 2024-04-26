    
def generate_possible_player_moves(game_state: list, player: int) -> list:
    pass

def generate_possible_pawn_moves(game_state: list, pos_x: int, pos_y: int):
    pass

# checks if direct (single) move from current pawn position to another is possible
# a direct (single) move is a move to free neighbour cell or jumping over 1 pawn into a free cell
def is_direct_pawn_move_possible(game_state: list, pos_x: int, pos_y: int, target_pos_x: int, target_pos_y: int) -> bool:
    dist_x = abs(pos_x - target_pos_x)
    dist_y = abs(pos_y - target_pos_y)
    # move requires moving more than 2 rows/columns so it's not direct move
    if (dist_x > 2 or dist_y > 2):
        return False
    
    if (dist_x == 0 and dist_y == 0):
        return False
    
    
    
if __name__ == "__main__":
    pass