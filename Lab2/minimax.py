import copy
from node import Node
from game import Game
from heuristics import Heuristics
from halma import generate_possible_player_moves, is_player_win

# def create_decision_tree(game: Game, depth: int) -> Node:
#     pass
    
        
# note: return tuple (node, best_move=(x,y))
def minimax(game: Game, depth: int, player_num: int, maximize: bool, evaluate_func):
    node = Node(game)
    if (is_player_win(game, player_num)):
        node.value = float('inf') if maximize else -float('inf')
        return (node, None)
    if (depth == 0):
        node.evaluate_game(player_num, evaluate_func)
        return (node, None)
    
    possible_moves = generate_possible_player_moves(game, player_num)

    best_move = None
    best_value = -float('inf') if maximize else float('inf')
    for move in possible_moves:
        game_after_move = copy.deepcopy(game)
        # print(game)
        # print(game_after_move)
        # try:
        game_after_move.move_pawn(player_num, move[0], move[1], move[2][0], move[2][1])
        # except ValueError:
        #     print(game_after_move)
        #     print(f'{move}/n')
        #     print(f'gracz {player_num}')
        #     print(f'pionek ktorego chce ruszyc {game_after_move.get_cell_val(move[0], move[1])}')
        #     print(f'miejsce na ktore chce isc {game_after_move.get_cell_val(move[2][0], move[2][1])}')
            
        # player_num = 2 if player_num == 1 else 1
        child_node, _ = minimax(game_after_move, depth - 1, player_num, not maximize, evaluate_func)
        # node.add_child(child_node, move)
        if (maximize):
            if (best_value < child_node.value):
                best_value = child_node.value
                best_move = move
        else:
            if (best_value > child_node.value):
                best_value = child_node.value
                best_move = move
    # print(node, best_move)
    return (node, best_move)

def minimax2(game: Game, depth: int, player_num: int, maximize: bool, evaluate_func):
    best_move = None
    if (is_player_win(game, player_num)):
        best_value = float('inf') if maximize else -float('inf')
        return (best_value, best_move)
    if (depth == 0):
        value = evaluate_func(game, player_num)
        return (value, best_move)
    
    possible_moves = generate_possible_player_moves(game, player_num)
    best_value = -float('inf') if maximize else float('inf')
    
    next_player_num = 1 if player_num == 2 else 2
    
    for move in possible_moves:
        game_after_move = copy.deepcopy(game)
        game_after_move.move_pawn(player_num, move[0], move[1], move[2][0], move[2][1])
        
        value, _ = minimax2(game_after_move, depth - 1, next_player_num, not maximize, evaluate_func)
        if (maximize):
            if (best_value < value):
                best_value = value
                best_move = move
        else:
            if (best_value > value):
                best_value = value
                best_move = move
    return (value, best_move)

if __name__ == "__main__":
    pass
    
        
        