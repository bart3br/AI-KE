from game import Game
from halma import generate_possible_player_moves, is_player_win

def minimax(game: Game, depth: int, player_num: int, maximize: bool, evaluate_func):
    best_move = None
    # check for win
    if (is_player_win(game, player_num)):
        best_value = float('inf') if maximize else -float('inf')
        return (best_value, None)
    # check for depth limit and evaluate if limit reached
    if (depth == 0):
        value = evaluate_func(game, player_num)
        return (value, None)
    
    player_turn = game.turn
    possible_moves = generate_possible_player_moves(game, player_turn)
    best_value = -float('inf') if maximize else float('inf')
    
    for move in possible_moves:
        # making a move and calling minimax recursively
        game.move_pawn(player_turn, move[0], move[1], move[2][0], move[2][1])
        value, _ = minimax(game, depth - 1, player_num, not maximize, evaluate_func)
        # reversing move as minimax works like DFS
        game.move_pawn_reverse(player_turn, move[0], move[1], move[2][0], move[2][1])
        if (maximize):
            if (best_value < value):
                best_value = value
                best_move = move
        else:
            if (best_value > value):
                best_value = value
                best_move = move
    return (value, best_move)

def alpha_beta_puring(game: Game, depth: int, player_num: int, maximize: bool, evaluate_func):
    pass

if __name__ == "__main__":
    pass
    
        
        