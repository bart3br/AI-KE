from game import Game
from halma import generate_possible_player_moves, is_player_win

def minimax(game: Game, depth: int, player_num: int, maximize: bool, evaluate_func):
    best_move = None
    player_turn = game.turn
    # check for win
    if (is_player_win(game, player_turn)):
        best_value = float('inf') if maximize else -float('inf')
        return (best_value, None)
    # check for depth limit and evaluate if limit reached
    if (depth == 0):
        value = evaluate_func(game, player_num)
        return (value, None)
    
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

def minimax_alpha_beta_puring(game: Game, depth: int, player_num: int, maximize: bool, evaluate_func ,alfa: float = float('-inf'), beta: float = float('inf')):
    best_move = None
    player_turn = game.turn
    # check for win
    if (is_player_win(game, player_turn)):
        best_value = float('inf') if maximize else -float('inf')
        return (best_value, None)
    # check for depth limit and evaluate if limit reached
    if (depth == 0):
        value = evaluate_func(game, player_num)
        return (value, None)
    
    possible_moves = generate_possible_player_moves(game, player_turn)
    best_value = -float('inf') if maximize else float('inf')
    
    for move in possible_moves:
        # making a move and calling minimax recursively
        game.move_pawn(player_turn, move[0], move[1], move[2][0], move[2][1])
        value, _ = minimax_alpha_beta_puring(game, depth - 1, player_num, not maximize, evaluate_func, alfa, beta)
        # reversing move as minimax works like DFS
        game.move_pawn_reverse(player_turn, move[0], move[1], move[2][0], move[2][1])
        if (maximize):
            if (best_value < value):
                best_value = value
                best_move = move
            
            alfa = max(value, alfa)
            if (beta <= alfa):
                return (alfa, best_move)
        else:
            if (best_value > value):
                best_value = value
                best_move = move
            beta = min(value, beta)
            if (beta <= alfa):
                return (beta, best_move)
    return (value, best_move)

if __name__ == "__main__":
    pass
    
        
        