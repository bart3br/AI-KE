from constants import EMPTY_CELL_VALUE

class Game:
    def __init__(self, game_state: list) -> None:
        self.board = []
        self.__init_board(game_state)
        self.turn = 1
        self.winner = 0
        self.BOARD_SIZE = len(self.board)
        
    def __init_board(self, game_state: list) -> None:
        for i in range(len(game_state)):
            self.board.append([])
            for j in range(len(game_state[i])):
                self.board[i].append(int(game_state[i][j]))
                    
                
    def __str__(self) -> str:
        board_str = f'player_turn={self.turn}, winner={self.winner}\n'
        for line in self.board:
            for cell in line:
                board_str += str(cell) + ' '
            board_str += '\n'
        return board_str
    
    def print_colorful_board(self) -> None:
        for line in self.board:
            for cell in line:
                if cell == 0:
                    # print empty cell with default color
                    print("0", end=" ")
                elif cell == 1:
                    # print 1st player's pawns with blue color
                    print("\033[94m1\033[0m", end=" ")
                elif cell == 2:
                    # print 2nd player's pawns with red color
                    print("\033[91m2\033[0m", end=" ")
            print()
        print()
    
    def get_cell_val(self, x: int, y: int) -> int:
        return self.board[x][y]
    
    def set_cell_val(self, x: int, y: int, value: int) -> None:
        self.board[x][y] = value
        
    def __switch_cells_vals(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]
        
    def move_pawn(self, player_num: int, pos_x: int, pos_y: int, target_pos_x: int, target_pos_y: int) -> None:
        if (self.get_cell_val(pos_x, pos_y) != player_num):
            raise ValueError('Trying to move other players pawn')
        if (self.get_cell_val(target_pos_x, target_pos_y) != EMPTY_CELL_VALUE):
            raise ValueError('Cell is already occupied by other pawn')
        self.__switch_cells_vals(pos_x, pos_y, target_pos_x, target_pos_y)
        self.turn = 2 if self.turn == 1 else 1
        
    def move_pawn_reverse(self, player_num: int, pos_x: int, pos_y: int, target_pos_x: int, target_pos_y: int) -> None:
        self.__switch_cells_vals(target_pos_x, target_pos_y, pos_x, pos_y)
        self.turn = 2 if self.turn == 1 else 1

    def check_for_winner(self, win_check_func) -> None:
        self.winner = win_check_func(self)             
        
# class Cell:
#     def __init__(self, pos_x: int, pos_y: int, symbol: int) -> None:
#         self.pos_x = pos_x
#         self.pos_y = pos_y
#         self.symbol = symbol
    
#     def __str__(self) -> str:
#         return f'{self.symbol}'

        
if __name__ == "__main__":
    pass
        