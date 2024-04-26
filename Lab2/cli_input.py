from constants import INITIAL_GAME_STATE_FILENAME

def read_initial_game_state() -> list:
    game_state = []
    with open(INITIAL_GAME_STATE_FILENAME, "r") as file:
        for line in file:
            # remove potential spaces from beginning and end of line
            # split the line into a list by spaces
            numbers_list = line.strip().split()
            game_state.append([int(num) for num in numbers_list])
    return game_state
    
    
def cli_print_initial_game_state(game_state: list) -> None:
    player_count = 0
    pawn_count = 0
    pawn_symbols = []
    for line in game_state:
        for num in line:
            if (num not in pawn_symbols and num != 0):
                pawn_symbols.append(num)
                player_count += 1
                pawn_count += 1
            elif (num != 0):
                pawn_count += 1
    print(f"Initial game state loaded from {INITIAL_GAME_STATE_FILENAME}")
    print(f"Number of players: {player_count}")
    print(f"Number of pawns for each player: {pawn_count // player_count}")
    print(''.join(['-' for i in range(0, 60)]))
  
if __name__ == "__main__":
    pass