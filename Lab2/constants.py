INITIAL_GAME_STATE_FILENAME = "initial_game_state.txt"
EMPTY_CELL_VALUE = 0
PLAYER1_VALUE = 1
PLAYER2_VALUE = 2
POSSIBLE_PAWN_MOVES = [(-1, -1), (-1, 0), (-1, 1), 
                       (0, -1), (0, 1),
                       (1, -1), (1, 0), (1, 1)]
POSSIBLE_PAWN_JUMPS = [(-2, -2), (-2, 0), (-2, 2),
                       (0, -2), (0, 2),
                       (2, -2), (2, 0), (2, 2)]

PLAYER1_STARTING_CELLS = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                          (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                          (2, 0), (2, 1), (2, 2), (2, 3),
                          (3, 0), (3, 1), (3, 2),
                          (4, 0), (4, 1)]

PLAYER2_STARTING_CELLS = [(15, 15), (15, 14), (15, 13), (15, 12), (15, 11),
                          (14, 15), (14, 14), (14, 13), (14, 12), (14, 11),
                          (13, 15), (13, 14), (13, 13), (13, 12),
                          (12, 15), (12, 14), (12, 13),
                          (11, 15), (11, 14)]

MAX_NUMBER_OF_POSSIBLE_MOVES = 400